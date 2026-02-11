from __future__ import annotations

import btspeak_client.audio_manager as audio_mod
from btspeak_client.audio_manager import AudioManager


def test_build_ffplay_filters_and_pitch():
    am = AudioManager()
    filters = am._build_ffplay_filters(volume=150, pan=-50, pitch=120)
    assert "volume=" in filters
    assert "pan=stereo" in filters
    assert "asetrate=" in filters
    assert "aresample=44100" in filters
    assert "atempo=" in filters


def test_resolve_sound_prefers_absolute(tmp_path):
    am = AudioManager()
    sound = tmp_path / "sound.wav"
    sound.write_text("x", encoding="utf-8")
    assert am._resolve_sound(str(sound)) == str(sound)


def test_play_sound_with_ffplay_invokes_subprocess(monkeypatch, tmp_path):
    am = AudioManager()
    am._ffplay_path = "/usr/bin/ffplay"

    calls = {}

    class FakeProc:
        def poll(self):
            return None

        def terminate(self):
            return None

    def fake_popen(args, **kwargs):
        calls["args"] = args
        return FakeProc()

    monkeypatch.setattr(audio_mod.subprocess, "Popen", fake_popen)

    sound = tmp_path / "sound.wav"
    sound.write_text("x", encoding="utf-8")
    assert am._play_sound_with_ffplay(str(sound), volume=120, pan=0, pitch=100) is True
    assert calls["args"][0] == "/usr/bin/ffplay"


def test_add_and_start_playlist(monkeypatch, tmp_path):
    am = AudioManager()
    am._sound_roots = [tmp_path]
    track = tmp_path / "track.wav"
    track.write_text("x", encoding="utf-8")

    started = {}

    def fake_run(files, *, loop=False, wait=False):
        started["files"] = files
        started["loop"] = loop
        return True

    monkeypatch.setattr(am, "_run_vlc_command", fake_run)

    assert am.add_playlist(
        playlist_id="p1",
        tracks=[str(track)],
        audio_type="music",
        shuffle_tracks=False,
        repeats=2,
        auto_start=True,
    )
    assert started["loop"] is False
    assert started["files"] == [str(track), str(track)]


def test_stop_all_audio_terminates_processes(monkeypatch):
    am = AudioManager()
    terminated = []

    class FakeProc:
        def poll(self):
            return None

        def terminate(self):
            terminated.append("yes")

    am._sound_processes = [FakeProc(), FakeProc()]

    monkeypatch.setattr(am, "stop_music", lambda: terminated.append("music"))
    monkeypatch.setattr(am, "stop_ambience", lambda: terminated.append("ambience"))

    am.stop_all_audio()
    assert "music" in terminated
    assert "ambience" in terminated
    assert len([t for t in terminated if t == "yes"]) == 2


def test_set_music_volume_applies_when_playing():
    am = AudioManager()
    calls = []

    class FakeVLC:
        def send_command(self, command):
            calls.append(command)

    am._vlc = FakeVLC()
    am._current_music = "/tmp/music.ogg"

    am.set_music_volume(120)
    assert calls[-1] == "volume 120"


def test_set_ambience_volume_applies_when_playing():
    am = AudioManager()
    calls = []

    class FakeVLC:
        def send_command(self, command):
            calls.append(command)

    am._vlc = FakeVLC()
    am._current_ambience = "/tmp/ambience.ogg"

    am.set_ambience_volume(80)
    assert calls[-1] == "volume 80"
