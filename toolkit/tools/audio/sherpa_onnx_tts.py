"""Sherpa-ONNX local text-to-speech provider tool (offline, multilingual incl. Hindi).

Why this exists: the stock ``piper_tts`` tool shells out to the ``piper`` CLI
and defaults to English. Native Indian-language narration (Hindi first) needs
voices that the Piper CLI install path does not ship. sherpa-onnx runs the same
Piper VITS voices (and Kokoro v1.0) fully offline from a pip wheel, with model
bundles hosted on GitHub releases (reachable where Hugging Face is not).

Voices are referenced by short ids (see ``VOICES``). Model bundles live under
``$SHERPA_ONNX_TTS_MODELS`` (default ``~/.openmontage/models/sherpa-onnx``).
Download them with::

    python -m tools.audio.sherpa_onnx_tts --download hi_rohan hi_kokoro

The tool joins automatically into ``tts_selector`` via the registry.
"""

from __future__ import annotations

import os
import tarfile
import time
import urllib.request
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

_RELEASE = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/"

# id -> bundle metadata. kind: "vits" (Piper) or "kokoro".
VOICES: dict[str, dict[str, Any]] = {
    "hi_rohan": {
        "bundle": "vits-piper-hi_IN-rohan-medium", "kind": "vits",
        "onnx": "hi_IN-rohan-medium.onnx", "sid": 0, "language": "hi",
        "gender": "male", "license": "IITM IndicTTS EULA (royalty-free; keep IITM notice)",
        "notes": "Native Hindi male (IndicTTS Hindi Mono Male). Warm, mature. Best default for Hindi.",
    },
    "hi_pratham": {
        "bundle": "vits-piper-hi_IN-pratham-medium", "kind": "vits",
        "onnx": "hi_IN-pratham-medium.onnx", "sid": 0, "language": "hi",
        "gender": "male", "license": "see MODEL_CARD in bundle",
        "notes": "Hindi male, faster delivery.",
    },
    "hi_priyamvada": {
        "bundle": "vits-piper-hi_IN-priyamvada-medium", "kind": "vits",
        "onnx": "hi_IN-priyamvada-medium.onnx", "sid": 0, "language": "hi",
        "gender": "female", "license": "see MODEL_CARD in bundle",
        "notes": "Hindi female.",
    },
    # Kokoro v1.0 (Apache-2.0). Hindi via espeak-ng phonemes; one bundle, many speakers.
    "hi_kokoro_psi": {"bundle": "kokoro-multi-lang-v1_0", "kind": "kokoro", "sid": 34, "language": "hi",
                       "gender": "male", "license": "Apache-2.0", "notes": "Kokoro hm_psi"},
    "hi_kokoro_omega": {"bundle": "kokoro-multi-lang-v1_0", "kind": "kokoro", "sid": 33, "language": "hi",
                         "gender": "male", "license": "Apache-2.0", "notes": "Kokoro hm_omega"},
    "hi_kokoro_alpha": {"bundle": "kokoro-multi-lang-v1_0", "kind": "kokoro", "sid": 31, "language": "hi",
                         "gender": "female", "license": "Apache-2.0", "notes": "Kokoro hf_alpha"},
    "hi_kokoro_beta": {"bundle": "kokoro-multi-lang-v1_0", "kind": "kokoro", "sid": 32, "language": "hi",
                        "gender": "female", "license": "Apache-2.0", "notes": "Kokoro hf_beta"},
    "en_kokoro_heart": {"bundle": "kokoro-multi-lang-v1_0", "kind": "kokoro", "sid": 3, "language": "en",
                         "gender": "female", "license": "Apache-2.0", "notes": "Kokoro af_heart"},
}

_KOKORO_LANG = {"hi": "hi", "en": "en-us"}


def models_dir() -> Path:
    return Path(os.environ.get("SHERPA_ONNX_TTS_MODELS", Path.home() / ".openmontage" / "models" / "sherpa-onnx"))


def _bundle_ready(voice_id: str) -> bool:
    v = VOICES[voice_id]
    d = models_dir() / v["bundle"]
    if v["kind"] == "vits":
        return (d / v["onnx"]).is_file() and (d / "tokens.txt").is_file()
    return (d / "model.onnx").is_file() and (d / "voices.bin").is_file()


def download(voice_ids: list[str]) -> list[str]:
    """Fetch model bundles from the sherpa-onnx GitHub release into models_dir()."""
    out = []
    root = models_dir()
    root.mkdir(parents=True, exist_ok=True)
    for vid in voice_ids:
        bundle = VOICES[vid]["bundle"]
        if (root / bundle).is_dir() and _bundle_ready(vid):
            out.append(f"{bundle}: already present")
            continue
        tmp = root / f"{bundle}.tar.bz2"
        urllib.request.urlretrieve(_RELEASE + f"{bundle}.tar.bz2", tmp)
        with tarfile.open(tmp, "r:bz2") as tf:
            tf.extractall(root, filter="data")
        tmp.unlink(missing_ok=True)
        out.append(f"{bundle}: downloaded")
    return out


class SherpaOnnxTTS(BaseTool):
    name = "sherpa_onnx_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "sherpa_onnx"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:sherpa_onnx", "python:soundfile"]
    install_instructions = (
        "Install sherpa-onnx and download a voice bundle (free, offline):\n"
        "  pip install sherpa-onnx soundfile\n"
        "  python -m tools.audio.sherpa_onnx_tts --download hi_rohan hi_kokoro_psi\n"
        "Bundles are fetched from GitHub releases (k2-fsa/sherpa-onnx, tag tts-models) into\n"
        "~/.openmontage/models/sherpa-onnx (override with SHERPA_ONNX_TTS_MODELS)."
    )
    agent_skills = ["text-to-speech"]

    capabilities = ["text_to_speech", "offline_generation", "hindi_narration"]
    supports = {
        "voice_cloning": False,
        "multilingual": True,
        "offline": True,
        "native_audio": True,
        "languages": ["hi", "en"],
    }
    best_for = [
        "offline Hindi narration (native Piper Hindi voices)",
        "zero-cost local fallback for Indian-language voiceover",
    ]
    not_good_for = [
        "studio-grade emotional range (prefer cloud neural voices when configured)",
        "voice cloning",
    ]

    input_schema = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string", "description": "Text to speak. Devanagari for Hindi voices."},
            "voice": {"type": "string", "enum": sorted(VOICES), "default": "hi_rohan"},
            "voice_id": {"type": "string", "description": "Alias for voice (selector pass-through)."},
            "speed": {"type": "number", "default": 1.0, "minimum": 0.5, "maximum": 2.0},
            "output_path": {"type": "string"},
            "num_threads": {"type": "integer", "default": 2},
            "noise_scale": {"type": "number", "default": 0.667, "description": "Piper/VITS only: higher = livelier intonation (0.6-0.85 sensible)"},
            "noise_scale_w": {"type": "number", "default": 0.8, "description": "Piper/VITS only: higher = more varied phoneme timing (0.7-1.0)"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=2, ram_mb=1024, vram_mb=0, disk_mb=500, network_required=False)
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=[])
    idempotency_key_fields = ["text", "voice", "speed", "noise_scale", "noise_scale_w"]
    side_effects = ["writes audio file to output_path"]
    user_visible_verification = ["Listen for pronunciation and pacing; back-translate with Whisper for intelligibility"]

    _engines: dict[str, Any] = {}

    def get_status(self) -> ToolStatus:
        try:
            import sherpa_onnx  # noqa: F401
            import soundfile  # noqa: F401
        except Exception:
            return ToolStatus.UNAVAILABLE
        if any(_bundle_ready(v) for v in VOICES):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def available_voices(self) -> list[str]:
        return [v for v in VOICES if _bundle_ready(v)]

    def _engine(self, voice_id: str, threads: int, noise: float = 0.667, noise_w: float = 0.8):
        import sherpa_onnx

        v = VOICES[voice_id]
        key = f"{v['bundle']}:{threads}:{noise}:{noise_w}"
        if key in self._engines:
            return self._engines[key]
        d = models_dir() / v["bundle"]
        if v["kind"] == "vits":
            model_cfg = sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model=str(d / v["onnx"]), tokens=str(d / "tokens.txt"), data_dir=str(d / "espeak-ng-data"),
                    noise_scale=noise, noise_scale_w=noise_w,
                ),
                num_threads=threads,
            )
        else:
            model_cfg = sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=str(d / "model.onnx"), voices=str(d / "voices.bin"), tokens=str(d / "tokens.txt"),
                    data_dir=str(d / "espeak-ng-data"), lexicon=str(d / "lexicon-us-en.txt"),
                    lang=_KOKORO_LANG.get(v["language"], ""),
                ),
                num_threads=threads,
            )
        eng = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=model_cfg))
        self._engines[key] = eng
        return eng

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="sherpa-onnx TTS not available. " + self.install_instructions)
        voice = inputs.get("voice") or inputs.get("voice_id") or "hi_rohan"
        if voice not in VOICES:
            return ToolResult(success=False, error=f"Unknown voice '{voice}'. Choose from {sorted(VOICES)}")
        if not _bundle_ready(voice):
            return ToolResult(success=False, error=f"Voice bundle for '{voice}' missing. Run: python -m tools.audio.sherpa_onnx_tts --download {voice}")
        start = time.time()
        try:
            import soundfile as sf

            out = Path(inputs.get("output_path", "tts_output.wav"))
            out.parent.mkdir(parents=True, exist_ok=True)
            eng = self._engine(voice, int(inputs.get("num_threads", 2)),
                               float(inputs.get("noise_scale", 0.667)), float(inputs.get("noise_scale_w", 0.8)))
            audio = eng.generate(inputs["text"], sid=VOICES[voice]["sid"], speed=float(inputs.get("speed", 1.0)))
            if len(audio.samples) == 0:
                return ToolResult(success=False, error="TTS produced empty audio")
            sf.write(str(out), audio.samples, audio.sample_rate, subtype="PCM_16")
            dur = len(audio.samples) / audio.sample_rate
        except Exception as exc:  # pragma: no cover - runtime path
            return ToolResult(success=False, error=f"sherpa-onnx generation failed: {exc}")
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "voice": voice,
                "language": VOICES[voice]["language"],
                "license": VOICES[voice]["license"],
                "sample_rate": audio.sample_rate,
                "audio_duration_seconds": round(dur, 3),
                "output": str(out),
                "format": "wav",
            },
            artifacts=[str(out)],
            model=VOICES[voice]["bundle"],
            duration_seconds=round(time.time() - start, 2),
        )


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Manage sherpa-onnx TTS voice bundles")
    ap.add_argument("--download", nargs="+", metavar="VOICE", help=f"voice ids: {', '.join(VOICES)}")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.download:
        for line in download(a.download):
            print(line)
    if a.list or not a.download:
        for vid, v in VOICES.items():
            print(f"{vid:18} {'READY' if _bundle_ready(vid) else 'missing':8} {v['gender']:6} {v['notes']}")
