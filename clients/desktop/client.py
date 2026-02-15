"""
Play Palace v11 Client

A wxPython-based client for Play Palace with websocket support.
Features:
- Menu list with multiletter navigation (toggle-able)
- Chat input
- History display
- Alt+M shortcut to focus menu
"""

import argparse
import os
import sys
from pathlib import Path


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="PlayPalace desktop client")
    parser.add_argument(
        "--debug-events",
        action="store_true",
        help="Emit structured JSON event logs to stdout for troubleshooting.",
    )
    return parser.parse_args(argv)


def _ensure_repo_root_on_path() -> Path:
    root = Path(__file__).resolve().parents[2]
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def _configure_debug_logging() -> None:
    from shared.debug_logging import install_json_logger

    install_json_logger(logger_name="playpalace.events", stream=sys.stdout)


def main(argv=None):
    """Main entry point for the Play Palace client."""
    args = _parse_args(argv)
    _ensure_repo_root_on_path()
    if args.debug_events:
        os.environ["PLAYPALACE_DEBUG_EVENTS"] = "1"

    import wx
    from ui import MainWindow
    from ui.login_dialog import LoginDialog

    if args.debug_events:
        _configure_debug_logging()

    app = wx.App(False)

    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.ShowModal() == wx.ID_OK:
        credentials = login_dialog.get_credentials()
        login_dialog.Destroy()

        # Create main window with credentials
        frame = MainWindow(credentials)
        frame.Show()
        app.MainLoop()
    else:
        # User cancelled login
        login_dialog.Destroy()


if __name__ == "__main__":
    main()
