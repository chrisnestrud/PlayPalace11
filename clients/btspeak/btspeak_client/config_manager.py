"""Configuration manager for Play Palace client.

Handles client-side configuration including:
- Server management with user accounts (identities.json - private)
- Global default options (option_profiles.json - shareable)
- Per-server option overrides (option_profiles.json - shareable)
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlsplit, urlunsplit

from .config_schemas import Identity, Identities, Server, UserAccount, validate_identities

TABLE_SECURITY_MODE_NEVER = "never"
TABLE_SECURITY_DEFAULT_TEXT = ""


def _normalize_key_path(key_path: str | tuple[str, ...] | list[str]) -> list[str]:
  """Convert path inputs into a sanitized list of keys."""
  if isinstance(key_path, str):
    working = key_path
    if working and working[0] == "/":
      working = working[1:]
    if working and working[-1] == "/":
      working = working[:-1]
    if not working:
      return []
    return [segment for segment in working.split("/") if segment != ""]
  return [segment for segment in key_path if segment != ""]


def get_item_from_dict(dictionary: dict, key_path: (str, tuple), *, create_mode: bool = False):
  """Return the item in a dictionary, typically a nested layer dict.
  Optionally create keys that don't exist, or require the full path to exist already.
  This function supports an infinite number of layers."""
  normalized_path = _normalize_key_path(key_path)
  scope = dictionary
  for index, segment in enumerate(normalized_path):
    layer = segment
    if layer not in scope:
      if not create_mode:
        prefix = "/".join(normalized_path[:index]) if index > 0 else "root dictionary"
        raise KeyError(f"Key '{layer}' not in {prefix}.")
      scope[layer] = {}
    scope = scope[layer]
  return scope


def set_item_in_dict(dictionary: dict, key_path: (str, tuple), value, *, create_mode: bool = False) -> bool:
  """Modify the value of an item in a dictionary.
  Optionally create keys that don't exist, or require the full path to exist already.
  This function supports an infinite number of layers."""
  normalized_path = _normalize_key_path(key_path)
  if not normalized_path:
    raise ValueError("No dictionary key path was specified.")
  final_key = normalized_path.pop(-1)
  obj = get_item_from_dict(dictionary, normalized_path, create_mode=create_mode)
  if not isinstance(obj, dict):
    raise TypeError(f"Expected type 'dict', instead got '{type(obj)}'.")
  if not create_mode and final_key not in obj:
    raise KeyError(f"Key '{final_key}' not in dictionary '{normalized_path}'.")
  obj[final_key] = value
  return True


def delete_item_from_dict(dictionary: dict, key_path: (str, tuple), *, delete_empty_layers: bool = True) -> bool:
  """Delete an item in a dictionary.
  Optionally delete layers that are empty.
  This function supports an infinite number of layers."""
  normalized_path = _normalize_key_path(key_path)
  if not normalized_path:
    raise ValueError("No dictionary key path was specified.")
  final_key = normalized_path.pop(-1)
  obj = get_item_from_dict(dictionary, normalized_path)
  if not isinstance(obj, dict):
    raise TypeError(f"Expected type 'dict', instead got '{type(obj)}'.")
  if final_key not in obj:
    return False
  del obj[final_key]
  if not delete_empty_layers:
    return True
  # Walk from deepest to shallowest, removing empty dicts
  for depth in range(len(normalized_path), 0, -1):
    try:
      current = get_item_from_dict(dictionary, normalized_path[:depth])
      if isinstance(current, dict) and not current:
        if depth == 1:
          del dictionary[normalized_path[0]]
        else:
          parent = get_item_from_dict(dictionary, normalized_path[:depth - 1])
          del parent[normalized_path[depth - 1]]
    except KeyError:
      break
  return True


class ConfigManager:
    """Manages client configuration and per-server settings.

    Uses two separate files:
    - identities.json: Contains servers with user accounts (private, not shareable)
    - option_profiles.json: Contains client options (shareable, no credentials)
    """

    def __init__(self, base_path: Optional[Path] = None):
        """Initialize the config manager.

        Args:
            base_path: Base directory path. Defaults to ~/.playpalace/
        """
        if base_path is None:
            base_path = Path.home() / ".playpalace"

        self.base_path = base_path
        self.identities_path = base_path / "identities.json"
        self.profiles_path = base_path / "option_profiles.json"

        self.identities = self._load_identities()
        self.profiles = self._load_profiles()

    def _load_identities(self) -> Dict[str, Any]:
        """Load identities from file (servers with user accounts)."""
        if self.identities_path.exists():
            try:
                with open(self.identities_path, "r") as f:
                    raw = json.load(f)
                    validated = validate_identities(raw)
                    validated, was_migrated = self._migrate_identity_records(validated)
                    was_normalized = self._normalize_server_ports(validated)
                    if validated != raw:
                        self.identities = validated
                        self.save_identities()
                        print("Identities validated and saved.")
                    elif was_migrated:
                        self.identities = validated
                        self.save_identities()
                        print("Identities migrated and saved.")
                    elif was_normalized:
                        self.identities = validated
                        self.save_identities()
                        print("Identities normalized and saved.")
                    return validated
            except Exception as e:
                print(f"Error loading identities: {e}")
                return self._get_default_identities()

        return self._get_default_identities()

    def _get_default_identities(self) -> Dict[str, Any]:
        """Get default identities structure."""
        return Identities().model_dump()

    def _migrate_identity_records(self, identities: Dict[str, Any]) -> tuple[Dict[str, Any], bool]:
        """Migrate legacy per-server accounts into global identity records."""
        migrated = False
        identities.setdefault("identities", {})
        identities.setdefault("last_identity_id", None)

        if identities["identities"]:
            return identities, migrated

        known_signatures = set()
        for server in identities.get("servers", {}).values():
            for account in server.get("accounts", {}).values():
                signature = (
                    account.get("username", ""),
                    account.get("password", ""),
                    account.get("email", ""),
                    account.get("notes", ""),
                )
                if signature in known_signatures:
                    continue

                identity = Identity(
                    username=account.get("username", ""),
                    password=account.get("password", ""),
                    email=account.get("email", ""),
                    notes=account.get("notes", ""),
                )
                identities["identities"][identity.identity_id] = identity.model_dump()
                known_signatures.add(signature)
                migrated = True

        if migrated and identities.get("last_identity_id") is None and identities["identities"]:
            identities["last_identity_id"] = next(iter(identities["identities"].keys()))

        return identities, migrated

    @staticmethod
    def _extract_port_from_host(host: str) -> Optional[int]:
        host = str(host or "").strip()
        if not host:
            return None
        parsed = urlsplit(host if "://" in host else f"ws://{host}")
        return parsed.port

    def _normalize_port_for_host(self, host: str, port_value: Any) -> int:
        embedded = self._extract_port_from_host(host)
        if embedded is not None and 1 <= embedded <= 65535:
            return embedded
        try:
            port = int(port_value)
        except (TypeError, ValueError):
            return 8000
        if 1 <= port <= 65535:
            return port
        return 8000

    def _normalize_server_ports(self, identities: Dict[str, Any]) -> bool:
        changed = False
        for server in identities.get("servers", {}).values():
            host = str(server.get("host", ""))
            current_port = server.get("port", 8000)
            normalized = self._normalize_port_for_host(host, current_port)
            if current_port != normalized:
                server["port"] = normalized
                changed = True
        return changed

    def _load_profiles(self) -> Dict[str, Any]:
        """Load option profiles from file (shareable, no credentials)."""
        if not self.profiles_path.exists():
            return self._get_default_profiles()

        try:
            with open(self.profiles_path, "r") as f:
                profiles = json.load(f)
                # Migrate old combined config if needed
                return self._migrate_profiles(profiles)
        except Exception as e:
            print(f"Error loading profiles: {e}")
            return self._get_default_profiles()

    def _get_default_profiles(self) -> Dict[str, Any]:
        """Get default profiles structure (shareable)."""
        return {
            "client_options_defaults": {
                "audio": {"music_volume": 20, "ambience_volume": 20},
                "social": {
                    "mute_global_chat": False,
                    "mute_table_chat": False,
                    "include_language_filters_for_table_chat": False,
                    "chat_input_language": "English",
                    "language_subscriptions": {},
                },
                "interface": {
                    "invert_multiline_enter_behavior": False,
                    "play_typing_sounds": True,
                },
                "local_table": {
                    "start_as_visible": "always",
                    "start_with_password": TABLE_SECURITY_MODE_NEVER,
                    "default_password_text": TABLE_SECURITY_DEFAULT_TEXT,
                    "creation_notifications": {},
                },  # Will be populated dynamically
            },
            "server_options": {},  # server_id -> options_overrides dict
        }

    def _migrate_profiles(self, profiles: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate profiles to fix data issues."""
        migrations = (
            self._migrate_servers_structure,
            self._migrate_language_settings,
            self._migrate_table_creations,
        )
        needs_save = False
        for migration in migrations:
            if migration(profiles):
                needs_save = True
        if needs_save:
            self.profiles = profiles
            self.save_profiles()
            print("Profile migration completed and saved to disk.")
        return profiles

    def _migrate_servers_structure(self, profiles: Dict[str, Any]) -> bool:
        changed = False
        if "servers" in profiles and "server_options" not in profiles:
            profiles["server_options"] = {}
            for server_id, server_info in profiles["servers"].items():
                overrides = server_info.get("options_overrides")
                if overrides:
                    profiles["server_options"][server_id] = overrides
            del profiles["servers"]
            changed = True
            print("Migrated 'servers' to 'server_options' in profiles")
        profiles.setdefault("server_options", {})
        return changed

    def _migrate_language_settings(self, profiles: Dict[str, Any]) -> bool:
        changed = False
        defaults = profiles.get("client_options_defaults", {})
        if self._fix_language_section(defaults.get("social", {}), "default profile"):
            changed = True
        for server_id, overrides in profiles.get("server_options", {}).items():
            social = overrides.get("social", {})
            if self._fix_language_section(social, f"server {server_id}"):
                changed = True
        return changed

    def _fix_language_section(self, social: Dict[str, Any], label: str) -> bool:
        changed = False
        lang_subs = social.get("language_subscriptions")
        if isinstance(lang_subs, dict) and "Check" in lang_subs:
            lang_subs["Czech"] = lang_subs.pop("Check")
            changed = True
            print(f"Migrated language subscription: 'Check' -> 'Czech' in {label}")
        chat_lang = social.get("chat_input_language")
        if chat_lang == "Check":
            social["chat_input_language"] = "Czech"
            changed = True
            print(f"Migrated chat_input_language: 'Check' -> 'Czech' in {label}")
        return changed

    def _migrate_table_creations(self, profiles: Dict[str, Any]) -> bool:
        changed = False
        defaults = profiles.get("client_options_defaults", {})
        if self._move_table_creations(defaults, "default profile"):
            changed = True
        for server_id, overrides in profiles.get("server_options", {}).items():
            if self._move_table_creations(overrides, f"server {server_id}"):
                changed = True
        return changed

    def _move_table_creations(self, options: Dict[str, Any], label: str) -> bool:
        if "table_creations" not in options:
            return False
        table_creations_value = options.pop("table_creations")
        local_table = options.setdefault("local_table", {})
        new_local_table = {
            "start_as_visible": local_table.get("start_as_visible", "always"),
            "start_with_password": local_table.get("start_with_password", TABLE_SECURITY_MODE_NEVER),
            "default_password_text": local_table.get("default_password_text", TABLE_SECURITY_DEFAULT_TEXT),
            "creation_notifications": table_creations_value,
        }
        for key, value in local_table.items():
            if key not in new_local_table:
                new_local_table[key] = value
        options["local_table"] = new_local_table
        print(f"Migrated 'table_creations' -> 'local_table/creation_notifications' in {label}")
        return True

    def _deep_merge(
        self, base: Dict[str, Any], override: Dict[str, Any], override_wins: bool = True
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries with configurable precedence.

        Supports infinite nesting depth.

        Args:
            base: Base dictionary
            override: Dictionary to merge into base
            override_wins: If True, override values take precedence on conflicts.
                           If False, base values take precedence (override fills missing keys only).

        Returns:
            Merged dictionary
        """
        result = self._deep_copy(base)

        for key, value in override.items():
            if key not in result:
                result[key] = self._deep_copy(value)
            elif isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = self._deep_merge(result[key], value, override_wins)
            elif override_wins:
                result[key] = self._deep_copy(value)
            # else: base wins, keep existing value

        return result

    def save_identities(self):
        """Save identities to file."""
        try:
            # Create directory if it doesn't exist
            self.base_path.mkdir(parents=True, exist_ok=True)

            with open(self.identities_path, "w") as f:
                json.dump(self.identities, f, indent=2)
        except Exception as e:
            print(f"Error saving identities: {e}")

    def save_profiles(self):
        """Save option profiles to file."""
        try:
            # Create config directory if it doesn't exist
            self.base_path.mkdir(parents=True, exist_ok=True)

            with open(self.profiles_path, "w") as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def save(self):
        """Save both identities and profiles."""
        self.save_identities()
        self.save_profiles()

    # ========== Server Management ==========

    # ========== Identity Management ==========

    def get_all_identities(self) -> Dict[str, Dict[str, Any]]:
        """Get all saved identities."""
        return self.identities.get("identities", {})

    def get_identity_by_id(self, identity_id: str) -> Optional[Dict[str, Any]]:
        """Get an identity by ID."""
        return self.get_all_identities().get(identity_id)

    def get_last_identity_id(self) -> Optional[str]:
        """Get the last selected identity ID."""
        return self.identities.get("last_identity_id")

    def set_last_identity(self, identity_id: str):
        """Set the last selected identity ID."""
        self.identities["last_identity_id"] = identity_id
        self.save_identities()

    def add_identity(
        self,
        username: str,
        password: str,
        email: str = "",
        notes: str = "",
    ) -> str:
        """Add a new global identity and return its ID."""
        target = username.strip().casefold()
        for existing in self.get_all_identities().values():
            if str(existing.get("username", "")).strip().casefold() == target:
                raise ValueError("An identity with that username already exists.")
        identity = Identity(username=username, password=password, email=email, notes=notes)
        self.identities.setdefault("identities", {})
        self.identities["identities"][identity.identity_id] = identity.model_dump()
        self.save_identities()
        return identity.identity_id

    def delete_identity(self, identity_id: str):
        """Delete an identity and clear last selection if needed."""
        identities = self.identities.get("identities", {})
        if identity_id in identities:
            del identities[identity_id]
            if self.identities.get("last_identity_id") == identity_id:
                self.identities["last_identity_id"] = None
            self.save_identities()

    def get_last_server_id(self) -> Optional[str]:
        """Get ID of last connected server."""
        return self.identities.get("last_server_id")

    def get_last_account_id(self, server_id: str) -> Optional[str]:
        """Get ID of last used account for a server.

        Args:
            server_id: Server ID

        Returns:
            Account ID or None if not set
        """
        server = self.get_server_by_id(server_id)
        if server:
            return server.get("last_account_id")
        return None

    def get_server_by_id(self, server_id: str) -> Optional[Dict[str, Any]]:
        """Get server info by ID.

        Args:
            server_id: Unique server ID

        Returns:
            Server info dict or None if not found
        """
        return self.identities["servers"].get(server_id)

    def get_all_servers(self) -> Dict[str, Dict[str, Any]]:
        """Get all servers.

        Returns:
            Dict mapping server_id to server info
        """
        return self.identities["servers"]

    def add_server(
        self,
        name: str,
        host: str,
        port: int,
        notes: str = "",
    ) -> str:
        """Add a new server.

        Args:
            name: Server display name
            host: Server host address
            port: Server port
            notes: Optional notes about the server

        Returns:
            New server ID
        """
        server = Server(name=name, host=host, port=port, notes=notes)
        server_id = server.server_id
        self.identities["servers"][server_id] = server.model_dump()
        self.save_identities()
        return server_id

    def update_server(
        self,
        server_id: str,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        notes: Optional[str] = None,
    ):
        """Update server information.

        Args:
            server_id: Server ID
            name: New server name (if provided)
            host: New host address (if provided)
            port: New port (if provided)
            notes: New notes (if provided)
        """
        if server_id not in self.identities["servers"]:
            return

        server = self.identities["servers"][server_id]
        if name is not None:
            server["name"] = name
        if host is not None:
            server["host"] = host
        if port is not None:
            server["port"] = port
        if notes is not None:
            server["notes"] = notes
        self.save_identities()

    def delete_server(self, server_id: str):
        """Delete a server and all its accounts.

        Args:
            server_id: Server ID to delete
        """
        if server_id in self.identities["servers"]:
            del self.identities["servers"][server_id]
            # Clear last_server_id if it was this server
            if self.identities.get("last_server_id") == server_id:
                self.identities["last_server_id"] = None
            self.save_identities()

    def get_server_display_name(self, server_id: str) -> str:
        """Get display name for a server.

        Args:
            server_id: Server ID

        Returns:
            Display name
        """
        server = self.get_server_by_id(server_id)
        if server:
            return server.get("name", "Unknown Server")
        return "Unknown Server"

    def get_server_url(self, server_id: str) -> Optional[str]:
        """Build WebSocket URL for a server.

        Args:
            server_id: Server ID

        Returns:
            WebSocket URL or None if server not found
        """
        server = self.get_server_by_id(server_id)
        if not server:
            return None

        host = str(server.get("host", "")).strip()
        if not host:
            return None

        port = self._normalize_port_for_host(host, server.get("port", 8000))

        def with_port(scheme: str, netloc: str, path: str = "", query: str = "", fragment: str = "") -> str:
            parsed_netloc = urlsplit(f"{scheme}://{netloc}")
            if parsed_netloc.port is None:
                if parsed_netloc.hostname:
                    hostname = parsed_netloc.hostname
                    if ":" in hostname and not hostname.startswith("["):
                        hostname = f"[{hostname}]"
                    userinfo = ""
                    if parsed_netloc.username:
                        userinfo = parsed_netloc.username
                        if parsed_netloc.password:
                            userinfo += f":{parsed_netloc.password}"
                        userinfo += "@"
                    netloc = f"{userinfo}{hostname}:{port}"
                else:
                    netloc = f"{netloc}:{port}"
            return urlunsplit((scheme, netloc, path, query, fragment))

        # Host may already include a ws/wss URL with path/query.
        if "://" in host:
            parsed = urlsplit(host)
            scheme = (parsed.scheme or "ws").lower()
            netloc = parsed.netloc or parsed.path
            path = parsed.path if parsed.netloc else ""
            return with_port(scheme, netloc, path=path, query=parsed.query, fragment=parsed.fragment)

        # Bare host form (hostname, hostname:port, or [ipv6]:port).
        parsed = urlsplit(f"ws://{host}")
        return with_port("ws", parsed.netloc or host, path=parsed.path, query=parsed.query, fragment=parsed.fragment)

    def set_last_server(self, server_id: str):
        """Set the last connected server.

        Args:
            server_id: Server ID
        """
        self.identities["last_server_id"] = server_id
        self.save_identities()

    # ========== Certificate Trust Management ==========

    def get_trusted_certificate(self, server_id: str) -> Optional[Dict[str, Any]]:
        """Return trusted certificate metadata for a server."""
        server = self.get_server_by_id(server_id)
        if server:
            return server.get("trusted_certificate")
        return None

    def set_trusted_certificate(self, server_id: str, cert_info: Dict[str, Any]) -> None:
        """Store trusted certificate metadata for a server."""
        server = self.get_server_by_id(server_id)
        if not server:
            return
        server["trusted_certificate"] = cert_info
        self.save_identities()

    def clear_trusted_certificate(self, server_id: str) -> None:
        """Remove stored certificate metadata for a server."""
        server = self.get_server_by_id(server_id)
        if not server:
            return
        if "trusted_certificate" in server:
            server["trusted_certificate"] = None
            self.save_identities()

    # ========== Account Management ==========

    def get_server_accounts(self, server_id: str) -> Dict[str, Dict[str, Any]]:
        """Get all accounts for a server.

        Args:
            server_id: Server ID

        Returns:
            Dict mapping account_id to account info
        """
        server = self.get_server_by_id(server_id)
        if server:
            return server.get("accounts", {})
        return {}

    def get_account_by_id(
        self, server_id: str, account_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get account info by ID.

        Args:
            server_id: Server ID
            account_id: Account ID

        Returns:
            Account info dict or None if not found
        """
        server = self.get_server_by_id(server_id)
        if server:
            return server.get("accounts", {}).get(account_id)
        return None

    def add_account(
        self,
        server_id: str,
        username: str,
        password: str,
        email: str = "",
        notes: str = "",
    ) -> Optional[str]:
        """Add a new account to a server.

        Args:
            server_id: Server ID
            username: Account username
            password: Account password
            email: Optional email address
            notes: Optional notes about the account

        Returns:
            New account ID, or None if server not found
        """
        if server_id not in self.identities["servers"]:
            return None

        account = UserAccount(
            username=username, password=password, email=email, notes=notes
        )
        account_id = account.account_id
        if "accounts" not in self.identities["servers"][server_id]:
            self.identities["servers"][server_id]["accounts"] = {}

        self.identities["servers"][server_id]["accounts"][account_id] = account.model_dump()
        self.save_identities()
        return account_id

    def update_account(
        self,
        server_id: str,
        account_id: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        """Update account information.

        Args:
            server_id: Server ID
            account_id: Account ID
            username: New username (if provided)
            password: New password (if provided)
            email: New email address (if provided)
            notes: New notes (if provided)
        """
        account = self.get_account_by_id(server_id, account_id)
        if not account:
            return

        if username is not None:
            account["username"] = username
        if password is not None:
            account["password"] = password
        if email is not None:
            account["email"] = email
        if notes is not None:
            account["notes"] = notes
        self.save_identities()

    def delete_account(self, server_id: str, account_id: str):
        """Delete an account from a server.

        Args:
            server_id: Server ID
            account_id: Account ID to delete
        """
        server = self.get_server_by_id(server_id)
        if server and account_id in server.get("accounts", {}):
            del server["accounts"][account_id]
            # Clear last_account_id if it was this account
            if server.get("last_account_id") == account_id:
                server["last_account_id"] = None
            self.save_identities()

    def set_last_account(self, server_id: str, account_id: str):
        """Set the last used account for a server.

        Args:
            server_id: Server ID
            account_id: Account ID
        """
        self.identities["last_server_id"] = server_id
        server = self.get_server_by_id(server_id)
        if server:
            server["last_account_id"] = account_id
        self.save_identities()

    def get_client_options(self, server_id: Optional[str] = None) -> Dict[str, Any]:
        """Get client options for a server (defaults + overrides).

        Args:
            server_id: Server ID, or None for just defaults

        Returns:
            Complete options dict with overrides applied
        """
        # Start with defaults
        options = self._deep_copy(self.profiles["client_options_defaults"])

        # Apply server-specific overrides if provided
        if server_id and server_id in self.profiles.get("server_options", {}):
            overrides = self.profiles["server_options"][server_id]
            options = self._deep_merge(options, overrides)

        return options

    def set_client_option(
        self, key_path: str, value: Any, server_id: Optional[str] = None, *, create_mode: bool = False
    ):
        """Set a client option (either default or server-specific override).

        Args:
            key_path: Path to the option (e.g., "audio/music_volume", "social/language_subscriptions/English")
            value: Option value
            server_id: Server ID for override, or None for default
            create_mode: If True, create intermediate dictionaries as needed
        """
        if server_id is None:
            # Set default
            target = self.profiles["client_options_defaults"]
        else:
            # Set server override
            if "server_options" not in self.profiles:
                self.profiles["server_options"] = {}
            target = self.profiles["server_options"].setdefault(server_id, {})

        success = set_item_in_dict(target, key_path, value, create_mode=create_mode)
        if success:
            self.save_profiles()

    def clear_server_override(self, server_id: str, key_path: str, *, delete_empty_layers: bool = True):
        """Clear a server-specific override (revert to default).

        Args:
            server_id: Server ID
            key_path: Path to the option (e.g., "audio/music_volume")
            delete_empty_layers: If True, delete intermediate dictionaries if empty
        """
        if server_id not in self.profiles.get("server_options", {}):
            return

        overrides = self.profiles["server_options"][server_id]

        success = delete_item_from_dict(overrides, key_path, delete_empty_layers=delete_empty_layers)
        if success:
            self.save_profiles()

    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy a nested dict/list structure."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        else:
            return obj
