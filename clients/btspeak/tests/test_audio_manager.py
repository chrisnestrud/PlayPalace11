from __future__ import annotations

import btspeak_client.audio_manager as am_mod
from btspeak_client.audio_manager import AudioManager


def test_build_ffplay_filters_contains_volume_pan_and_pitch_chain():
    manager = AudioManager()

    af = manager._build_ffplay_filters(volume=80, pan=25, pitch=125)

    assert "volume=0.800000" in af
    assert "pan=stereo|c0=0.750000*c0|c1=1.000000*c1" in af
    assert "asetrate=44100*1.250000" in af
    assert "aresample=44100" in af
    assert "atempo=0.800000" in af


def test_play_sound_uses_ffplay_when_modifiers_present(monkeypatch):
    manager = AudioManager()
    manager._ffplay_path = "/usr/bin/ffplay"

    monkeypatch.setattr(manager, "_resolve_sound", lambda name: "/tmp/sound.ogg")

    popen_calls = []

    class FakeProcess:
        def poll(self):
            return None

    def fake_popen(args, stdin=None, stdout=None, stderr=None):
        popen_calls.append(args)
        return FakeProcess()

    monkeypatch.setattr(am_mod.subprocess, "Popen", fake_popen)

    assert manager.play_sound("sound.ogg", volume=70, pan=-10, pitch=115) is True
    assert popen_calls
    assert popen_calls[0][0] == "/usr/bin/ffplay"
    assert "-af" in popen_calls[0]


def test_play_sound_falls_back_to_vlc_when_defaults(monkeypatch):
    manager = AudioManager()

    monkeypatch.setattr(manager, "_resolve_sound", lambda name: "/tmp/sound.ogg")
    monkeypatch.setattr(manager, "_run_vlc_command", lambda files, loop=False, wait=False: True)

    assert manager.play_sound("sound.ogg", volume=100, pan=0, pitch=100) is True


def test_play_sound_modifiers_fall_back_to_vlc_when_ffplay_missing(monkeypatch):
    manager = AudioManager()
    manager._ffplay_path = None

    monkeypatch.setattr(manager, "_resolve_sound", lambda name: "/tmp/sound.ogg")
    monkeypatch.setattr(manager, "_run_vlc_command", lambda files, loop=False, wait=False: True)

    assert manager.play_sound("sound.ogg", volume=50, pan=20, pitch=120) is True


def test_play_sound_missing_file_returns_false(monkeypatch):
    manager = AudioManager()
    monkeypatch.setattr(manager, "_resolve_sound", lambda name: None)
    assert manager.play_sound("missing.ogg", volume=90, pan=0, pitch=100) is False


def test_playlist_add_start_remove_round_trip(monkeypatch):
    manager = AudioManager()
    monkeypatch.setattr(manager, "_resolve_sound", lambda name: f"/tmp/{name}")
    monkeypatch.setattr(manager, "_run_vlc_command", lambda files, loop=False, wait=False: True)

    assert manager.add_playlist(
        playlist_id="pl1",
        tracks=["a.ogg", "b.ogg"],
        audio_type="music",
        shuffle_tracks=False,
        repeats=1,
        auto_start=False,
    )
    assert manager.start_playlist("pl1") is True
    assert manager.remove_playlist("pl1") is True


def test_playlist_add_empty_tracks_returns_false(monkeypatch):
    manager = AudioManager()
    monkeypatch.setattr(manager, "_resolve_sound", lambda name: None)
    assert manager.add_playlist(
        playlist_id="pl-empty",
        tracks=["missing.ogg"],
        audio_type="sound",
        shuffle_tracks=False,
        repeats=1,
        auto_start=False,
    ) is False
