import os
import time
from pathlib import Path

import gradio as gr

# heartlib gets installed during Pinokio install.json
# HeartMuLaGenPipeline lives under heartlib.pipelines
from heartlib.pipelines.music_generation import HeartMuLaGenPipeline

import torch


APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"
OUTPUTS_DIR = APP_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

_PIPELINE_CACHE = {}


def _auto_device_str() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def _load_text_file(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def _get_pipeline(model_path: str, version: str, device_str: str):
    mp = str(Path(model_path).resolve())
    key = (mp, version, device_str)
    if key in _PIPELINE_CACHE:
        return _PIPELINE_CACHE[key]

    device = torch.device(device_str)
    # Safe defaults: fp16 on CUDA, fp32 on CPU
    dtype = torch.float16 if device.type == "cuda" else torch.float32

    pipe = HeartMuLaGenPipeline.from_pretrained(
        pretrained_path=mp,
        device=device,
        dtype=dtype,
        version=version,
    )
    _PIPELINE_CACHE[key] = pipe
    return pipe


def generate(
    model_path: str,
    lyrics_text: str,
    tags_text: str,
    lyrics_file,
    tags_file,
    save_name: str,
    max_audio_length_ms: int,
    topk: int,
    temperature: float,
    cfg_scale: float,
    version: str,
    device_choice: str,
):
    # Prefer uploaded files if present
    if lyrics_file is not None:
        lyrics_text = _load_text_file(lyrics_file)
    if tags_file is not None:
        tags_text = _load_text_file(tags_file)

    lyrics_text = (lyrics_text or "").strip()
    if not lyrics_text:
        raise gr.Error("Lyrics are required (paste them or upload a lyrics file).")

    # README: tags are comma-separated without spaces
    tags_text = (tags_text or "").strip().replace(" ", "")

    model_path = (model_path or "").strip()
    if not model_path:
        raise gr.Error("model_path is required (e.g. ./ckpt).")

    device_str = device_choice
    if device_choice == "auto":
        device_str = _auto_device_str()

    pipe = _get_pipeline(model_path=model_path, version=version, device_str=device_str)

    out = OUTPUTS_DIR / (
        save_name.strip() if save_name and save_name.strip() else f"output_{int(time.time())}.wav"
    )
    # If user gave no extension, default to wav (mp3 requires ffmpeg-enabled backend)
    if out.suffix.lower() not in {".mp3", ".wav"}:
        out = out.with_suffix(".wav")

    try:
        # HeartMuLaGenPipeline is a HuggingFace Pipeline.
        # It saves audio in postprocess(save_path=...).
        pipe(
            {"lyrics": lyrics_text, "tags": tags_text},
            save_path=str(out),
            max_audio_length_ms=int(max_audio_length_ms),
            topk=int(topk),
            temperature=float(temperature),
            cfg_scale=float(cfg_scale),
        )
    except Exception as e:
        # Common gotcha: saving mp3 without ffmpeg/encoder support.
        if out.suffix.lower() == ".mp3":
            raise gr.Error(
                f"Generation ran but saving MP3 failed. Try a .wav save name (recommended), or add ffmpeg to the environment.\n\nError: {e}"
            )
        raise

    return str(out), str(out)


with gr.Blocks(title="HeartMuLa (HeartMuLaGen)") as demo:
    gr.Markdown(
        """
# HeartMuLa (HeartMuLaGen)

Generate music conditioned on **lyrics** and optional **comma-separated tags**.

- Default checkpoint folder: `./ckpt` (downloaded by `install.json`)
- Default lyric/tag examples live in `./assets/`

Tip: if MP3 saving fails, use `.wav` (more portable) or add ffmpeg to the env.
"""
    )

    with gr.Row():
        model_path = gr.Textbox(
            label="--model_path (required)",
            value=str(ASSETS_DIR.parent / "ckpt"),
            placeholder="./ckpt",
        )
        version = gr.Dropdown(["3B"], value="3B", label="--version")
        device_choice = gr.Dropdown(["auto", "cuda", "cpu"], value="auto", label="Device")

    with gr.Row():
        lyrics_file = gr.File(label="--lyrics (optional file)", file_types=[".txt"], type="filepath")
        tags_file = gr.File(label="--tags (optional file)", file_types=[".txt"], type="filepath")

    lyrics_text = gr.Textbox(
        label="Lyrics (paste here if not uploading)",
        value=_load_text_file(str(ASSETS_DIR / "lyrics.txt")),
        lines=16,
    )

    tags_text = gr.Textbox(
        label="Tags (comma-separated, no spaces)",
        value=_load_text_file(str(ASSETS_DIR / "tags.txt")).strip(),
        placeholder="piano,happy,wedding,synthesizer,romantic",
    )

    save_name = gr.Textbox(
        label="--save_path (filename inside ./outputs)",
        value="output.wav",
    )

    with gr.Accordion("Sampling & length", open=True):
        max_audio_length_ms = gr.Slider(10_000, 240_000, value=240_000, step=1000, label="--max_audio_length_ms")
        topk = gr.Slider(1, 200, value=50, step=1, label="--topk")
        temperature = gr.Slider(0.1, 2.0, value=1.0, step=0.05, label="--temperature")
        cfg_scale = gr.Slider(0.0, 5.0, value=1.5, step=0.1, label="--cfg_scale")

    run_btn = gr.Button("Generate")

    audio_out = gr.Audio(label="Output (playback)", type="filepath")
    file_out = gr.File(label="Output (download)")

    run_btn.click(
        fn=generate,
        inputs=[
            model_path,
            lyrics_text,
            tags_text,
            lyrics_file,
            tags_file,
            save_name,
            max_audio_length_ms,
            topk,
            temperature,
            cfg_scale,
            version,
            device_choice,
        ],
        outputs=[audio_out, file_out],
    )


demo.launch(
    server_name=os.environ.get("GRADIO_SERVER_NAME", "127.0.0.1"),
    server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
)
