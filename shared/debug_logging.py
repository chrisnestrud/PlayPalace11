"""Shared utilities for structured debug logging."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

__all__ = [
    "DebugLogContext",
    "install_json_logger",
    "is_debug_env_enabled",
    "summarize_event_packet",
    "estimate_packet_bytes",
]


_DEBUG_ENV_FLAG = "PLAYPALACE_DEBUG_EVENTS"
_JSON_DEFAULT_SKIP = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
    "asctime",
}


@dataclass
class DebugLogContext:
    """Structured context used when emitting event logs."""

    event: str
    table_id: str | None = None
    user_id: str | None = None
    username: str | None = None
    game: str | None = None
    correlation_id: str | None = None
    duration_ms: float | None = None
    payload_size: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


def is_debug_env_enabled(value: str | None = None) -> bool:
    """Return True when the shared debug logging env flag evaluates to true."""
    if value is None:
        value = os.environ.get(_DEBUG_ENV_FLAG)
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def summarize_event_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Return a sanitized summary of an input event packet."""
    event_type = str(packet.get("type", "unknown"))
    summary: dict[str, Any] = {"event_type": event_type}

    if event_type == "menu":
        summary["menu_id"] = packet.get("menu_id")
        summary["selection_id"] = packet.get("selection_id")
        summary["selection"] = packet.get("selection")
    elif event_type == "keybind":
        summary["key"] = packet.get("key")
        summary["menu_id"] = packet.get("menu_id")
        summary["menu_item_id"] = packet.get("menu_item_id")
        summary["menu_index"] = packet.get("menu_index")
        summary["control"] = bool(packet.get("control"))
        summary["alt"] = bool(packet.get("alt"))
        summary["shift"] = bool(packet.get("shift"))
    elif event_type == "editbox":
        text = packet.get("text") or ""
        summary["input_id"] = packet.get("input_id")
        summary["text_length"] = len(text)
    else:
        for key in ("menu_id", "input_id", "key"):
            if key in packet:
                summary[key] = packet.get(key)
    return summary


def estimate_packet_bytes(packet: Mapping[str, Any]) -> int:
    """Approximate the serialized byte size of a packet."""
    try:
        return len(json.dumps(packet, ensure_ascii=False))
    except (TypeError, ValueError):
        return len(str(packet))


def _stringify_unserializable(value: Any) -> str:
    return repr(value)


class _JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key in _JSON_DEFAULT_SKIP:
                continue
            if key.startswith("_"):
                continue
            payload[key] = value
        return json.dumps(payload, ensure_ascii=False, default=_stringify_unserializable)


def install_json_logger(
    *,
    logger_name: str,
    level: int = logging.DEBUG,
    stream=None,
    filters: Iterable[logging.Filter] | None = None,
) -> logging.Logger:
    """Install a JSON handler for the given logger."""
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    handler.setFormatter(_JSONFormatter())
    for log_filter in filters or ():
        handler.addFilter(log_filter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False
    logger.handlers.clear()
    logger.addHandler(handler)
    return logger
