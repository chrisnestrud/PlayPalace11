"""Dialog for trusting self-signed TLS certificates."""

from dataclasses import dataclass
from typing import Optional, Sequence

import wx


@dataclass
class CertificateInfo:
    """Structured information about a presented certificate."""

    host: str
    common_name: str
    sans: Sequence[str]
    issuer: str
    valid_from: str
    valid_to: str
    fingerprint: str  # Display-friendly fingerprint
    fingerprint_hex: str  # Raw hex without delimiters
    pem: str
    matches_host: bool


class CertificatePromptDialog(wx.Dialog):
    """Modal dialog prompting the user to trust an unverified certificate."""

    def __init__(self, parent, info: CertificateInfo):
        super().__init__(parent, title="Untrusted Certificate", size=(500, 420))
        self.info = info
        self._create_ui()
        self.CenterOnParent()

    def _create_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        intro = wx.StaticText(
            panel,
            label="The server presented a certificate that could not be verified.",
        )
        intro.Wrap(460)
        sizer.Add(intro, 0, wx.ALL | wx.EXPAND, 12)

        warning_text = (
            "Hostname matches certificate." if self.info.matches_host
            else f"Hostname mismatch: expected {self.info.host}."
        )
        warning = wx.StaticText(panel, label=warning_text)
        if not self.info.matches_host:
            warning.SetForegroundColour(wx.Colour(200, 50, 50))
        sizer.Add(warning, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        grid = wx.FlexGridSizer(0, 2, 4, 8)
        grid.AddGrowableCol(1, 1)

        def add_row(label, value):
            lbl = wx.StaticText(panel, label=label)
            lbl.SetFont(lbl.GetFont().Bold())
            grid.Add(lbl, 0, wx.ALIGN_TOP)
            text = wx.StaticText(panel, label=value)
            text.Wrap(360)
            grid.Add(text, 0, wx.ALIGN_TOP | wx.EXPAND)

        add_row("Server host:", self.info.host or "(unknown)")
        add_row("Common name:", self.info.common_name or "(none)")
        sans = ", ".join(self.info.sans) if self.info.sans else "(none)"
        add_row("Subject Alt Names:", sans)
        add_row("Issuer:", self.info.issuer or "(unknown)")
        add_row("Valid from:", self.info.valid_from or "(unknown)")
        add_row("Valid to:", self.info.valid_to or "(unknown)")
        add_row("Fingerprint (SHA-256):", self.info.fingerprint)

        sizer.Add(grid, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        info_text = wx.StaticText(
            panel,
            label="If you trust this certificate, PlayPalace will remember it and only reconnect if the fingerprint matches in the future.",
        )
        info_text.Wrap(460)
        sizer.Add(info_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        button_sizer = wx.StdDialogButtonSizer()
        trust_btn = wx.Button(panel, wx.ID_OK, "Trust Certificate")
        trust_btn.SetDefault()
        cancel_btn = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.AddButton(trust_btn)
        button_sizer.AddButton(cancel_btn)
        button_sizer.Realize()

        sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        panel.SetSizer(sizer)


@dataclass
class CertificateChangePromptInfo:
    """Context for prompting the user about a changed certificate."""

    host: str
    previous: Optional[CertificateInfo]
    current: CertificateInfo


class CertificateChangePromptDialog(wx.Dialog):
    """Dialog shown when the stored certificate fingerprint no longer matches."""

    HIGHLIGHT = wx.Colour(200, 50, 50)

    def __init__(self, parent, info: CertificateChangePromptInfo):
        super().__init__(parent, title="Certificate Changed", size=(580, 520))
        self.info = info
        self._trust_btn: Optional[wx.Button] = None
        self._create_ui()
        self.CenterOnParent()

    def _create_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        host = self.info.host or "this server"
        intro = wx.StaticText(
            panel,
            label=(
                f"PlayPalace previously trusted a different certificate for {host}.\n"
                "This could mean the server rotated certificates or someone is "
                "attempting to intercept your connection."
            ),
        )
        intro.Wrap(540)
        sizer.Add(intro, 0, wx.ALL | wx.EXPAND, 12)

        grid = wx.FlexGridSizer(0, 3, 6, 10)
        grid.AddGrowableCol(1, 1)
        grid.AddGrowableCol(2, 1)

        header_font = wx.Font(wx.FontInfo(10).Bold())
        grid.AddSpacer(0)
        prev_header = wx.StaticText(panel, label="Previously trusted")
        prev_header.SetFont(header_font)
        grid.Add(prev_header, 0, wx.ALIGN_CENTER_HORIZONTAL)
        new_header = wx.StaticText(panel, label="New certificate")
        new_header.SetFont(header_font)
        grid.Add(new_header, 0, wx.ALIGN_CENTER_HORIZONTAL)

        def format_value(text: Optional[str]) -> str:
            stripped = (text or "").strip()
            return stripped or "(unknown)"

        fields = (
            ("Common name", lambda cert: cert.common_name),
            ("Issuer", lambda cert: cert.issuer),
            ("Valid from", lambda cert: cert.valid_from),
            ("Valid to", lambda cert: cert.valid_to),
            ("Fingerprint (SHA-256)", lambda cert: cert.fingerprint),
            (
                "Subject Alt Names",
                lambda cert: ", ".join(cert.sans) if cert.sans else "(none)",
            ),
        )

        previous = self.info.previous
        current = self.info.current

        for label_text, extractor in fields:
            label = wx.StaticText(panel, label=label_text + ":")
            label.SetFont(label.GetFont().Bold())
            grid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)

            prev_value = format_value(extractor(previous) if previous else None)
            prev_text = wx.StaticText(panel, label=prev_value)
            prev_text.Wrap(220)
            grid.Add(prev_text, 0, wx.EXPAND)

            new_value = format_value(extractor(current))
            new_text = wx.StaticText(panel, label=new_value)
            new_text.Wrap(220)
            if previous is None or new_value != prev_value:
                new_text.SetForegroundColour(self.HIGHLIGHT)
            grid.Add(new_text, 0, wx.EXPAND)

        sizer.Add(grid, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 12)

        guidance = wx.StaticText(
            panel,
            label=(
                "Only continue if you confirmed the new fingerprint with the server "
                "administrator through a separate channel."
            ),
        )
        guidance.Wrap(540)
        sizer.Add(guidance, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        checkbox = wx.CheckBox(
            panel,
            label="I verified the new certificate details out-of-band and want to trust it.",
        )
        checkbox.Bind(wx.EVT_CHECKBOX, self._on_checkbox)
        sizer.Add(checkbox, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        button_sizer = wx.StdDialogButtonSizer()
        trust_btn = wx.Button(panel, wx.ID_OK, "Trust Replacement")
        trust_btn.Enable(False)
        self._trust_btn = trust_btn
        cancel_btn = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.AddButton(trust_btn)
        button_sizer.AddButton(cancel_btn)
        button_sizer.Realize()

        sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        panel.SetSizer(sizer)

    def _on_checkbox(self, event):
        if not self._trust_btn:
            return
        self._trust_btn.Enable(event.IsChecked())
