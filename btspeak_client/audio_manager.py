"""BTSpeak-backed audio playback for the CLI client."""

from __future__ import annotations

import random
import shutil
import subprocess
from pathlib import Path


class AudioManager:
    """Handles sound, music, ambience, and playlists via BTSpeak VLC helpers."""

    def __init__(self):
        self._vlc = None
        self._host = None
        self._playlists: dict[str, dict] = {}
        self._current_music: str | None = None
        self._current_ambience: str | None = None
        self._music_volume: int | None = None
        self._ambience_volume: int | None = None
        self._ffplay_path = shutil.which("ffplay")
        self._sound_processes: list[subprocess.Popen] = []

        try:
            from BTSpeak import AudioPlayers, host

            self._vlc = AudioPlayers.VLC()
            self._host = host
        except Exception:
            self._vlc = None
            self._host = None

        self._sound_roots = [Path(__file__).resolve().parent / "sounds"]

    @property
    def available(self) -> bool:
        return self._vlc is not None

    def _resolve_sound(self, name: str) -> str | None:
        candidate = Path(name)
        if candidate.is_absolute() and candidate.exists():
            return str(candidate)

        for root in self._sound_roots:
            path = root / name
            if path.exists():
                return str(path)
        return None

    def _run_vlc_command(self, files: list[str], *, loop: bool = False, wait: bool = False) -> bool:
        if not self._vlc or not files:
            return False

        command = self._vlc.make_command(files)
        command.addOption("intf", "rc")
        command.addOption("loop" if loop else "no-loop")
        command.addOption("no-random")
        if not wait:
            command.addOption("rc-host", f"{self._vlc.socket_host}:{self._vlc.socket_port}")
            command.start()
        else:
            command.run()
        return True

    def _reap_sound_processes(self) -> None:
        alive: list[subprocess.Popen] = []
        for process in self._sound_processes:
            if process.poll() is None:
                alive.append(process)
        self._sound_processes = alive

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, int(value)))

    def _make_pitch_tempo_filter(self, ratio: float) -> str:
        # ffmpeg atempo only supports factors within [0.5, 2.0], so split the adjustment.
        target = 1.0 / ratio
        factors: list[float] = []
        while target > 2.0:
            factors.append(2.0)
            target /= 2.0
        while target < 0.5:
            factors.append(0.5)
            target /= 0.5
        factors.append(target)
        return ",".join(f"atempo={factor:.6f}" for factor in factors)

    def _build_ffplay_filters(self, *, volume: int, pan: int, pitch: int) -> str:
        volume = self._clamp(volume, 0, 200)
        pan = self._clamp(pan, -100, 100)
        pitch = self._clamp(pitch, 10, 400)

        filters = [f"volume={volume / 100:.6f}"]

        pan_ratio = pan / 100.0
        left_gain = 1.0 - max(0.0, pan_ratio)
        right_gain = 1.0 + min(0.0, pan_ratio)
        filters.append(
            f"pan=stereo|c0={left_gain:.6f}*c0|c1={right_gain:.6f}*c1"
        )

        if pitch != 100:
            ratio = pitch / 100.0
            filters.append(f"asetrate=44100*{ratio:.6f}")
            filters.append("aresample=44100")
            filters.append(self._make_pitch_tempo_filter(ratio))

        return ",".join(filters)

    def _play_sound_with_ffplay(self, path: str, *, volume: int, pan: int, pitch: int) -> bool:
        if not self._ffplay_path:
            return False

        self._reap_sound_processes()
        af = self._build_ffplay_filters(volume=volume, pan=pan, pitch=pitch)
        process = subprocess.Popen(
            [
                self._ffplay_path,
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                "-af",
                af,
                path,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._sound_processes.append(process)
        return True

    def play_sound(self, name: str, volume: int = 100, pan: int = 0, pitch: int = 100) -> bool:
        path = self._resolve_sound(name)
        if not path:
            return False
        if volume != 100 or pan != 0 or pitch != 100:
            if self._play_sound_with_ffplay(path, volume=volume, pan=pan, pitch=pitch):
                return True
        return self._run_vlc_command([path], loop=False, wait=False)

    def play_music(self, name: str, looping: bool = True) -> bool:
        path = self._resolve_sound(name)
        if not path:
            return False
        self.stop_music()
        ok = self._run_vlc_command([path], loop=looping, wait=False)
        if ok:
            self._current_music = path
            if self._music_volume is not None:
                self._apply_volume(self._music_volume)
        return ok

    def stop_music(self) -> None:
        if not self._vlc:
            return
        self._vlc.send_command("stop")
        self._vlc.send_command("clear")
        self._current_music = None

    def play_ambience(self, intro: str | None, loop: str, outro: str | None = None) -> bool:
        del outro
        files: list[str] = []
        if intro:
            intro_path = self._resolve_sound(intro)
            if intro_path:
                files.append(intro_path)

        loop_path = self._resolve_sound(loop)
        if not loop_path:
            return False
        files.append(loop_path)

        self.stop_ambience()
        ok = self._run_vlc_command(files, loop=True, wait=False)
        if ok:
            self._current_ambience = loop_path
            if self._ambience_volume is not None:
                self._apply_volume(self._ambience_volume)
        return ok

    def stop_ambience(self) -> None:
        if not self._vlc:
            return
        self._vlc.send_command("stop")
        self._vlc.send_command("clear")
        self._current_ambience = None

    def _apply_volume(self, volume: int) -> None:
        if not self._vlc:
            return
        clamped = self._clamp(volume, 0, 200)
        try:
            self._vlc.send_command(f"volume {clamped}")
        except Exception:
            pass

    def set_music_volume(self, volume: int) -> None:
        self._music_volume = self._clamp(volume, 0, 200)
        if self._current_music:
            self._apply_volume(self._music_volume)

    def set_ambience_volume(self, volume: int) -> None:
        self._ambience_volume = self._clamp(volume, 0, 200)
        if self._current_ambience:
            self._apply_volume(self._ambience_volume)

    def add_playlist(
        self,
        *,
        playlist_id: str,
        tracks: list[str],
        audio_type: str,
        shuffle_tracks: bool,
        repeats: int,
        auto_start: bool,
    ) -> bool:
        resolved_tracks = [self._resolve_sound(track) for track in tracks]
        playable = [track for track in resolved_tracks if track]
        if not playable:
            return False

        self._playlists[playlist_id] = {
            "tracks": playable,
            "audio_type": audio_type,
            "shuffle_tracks": shuffle_tracks,
            "repeats": repeats,
        }
        if auto_start:
            return self.start_playlist(playlist_id)
        return True

    def start_playlist(self, playlist_id: str) -> bool:
        playlist = self._playlists.get(playlist_id)
        if not playlist:
            return False

        tracks = list(playlist["tracks"])
        if playlist["shuffle_tracks"]:
            random.shuffle(tracks)

        repeats = int(playlist["repeats"])
        loop = repeats == 0
        if repeats > 1:
            tracks = tracks * repeats

        if playlist.get("audio_type") == "music":
            self.stop_music()
            return self._run_vlc_command(tracks, loop=loop, wait=False)

        return self._run_vlc_command(tracks, loop=loop, wait=False)

    def remove_playlist(self, playlist_id: str) -> bool:
        return self._playlists.pop(playlist_id, None) is not None

    def remove_all_playlists(self) -> None:
        self._playlists.clear()

    def stop_all_audio(self) -> None:
        """Stop all currently playing music, ambience, and one-shot sounds."""
        self.stop_music()
        self.stop_ambience()
        self._reap_sound_processes()
        for process in self._sound_processes:
            try:
                process.terminate()
            except Exception:
                pass
        self._sound_processes = []
