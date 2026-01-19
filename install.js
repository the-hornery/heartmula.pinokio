module.exports = {
    run: [
        {
            method: "shell.run",
            params: {
                conda: {
                    path: "env",
                    python: "python=3.10"
                },
                message: [
                    "uv pip install -U pip",
                    "uv pip install -U huggingface_hub[cli]",
                    "uv pip install gradio pydub uvicorn[standard] websockets wsproto"
                ]
            }
        },
        {
            "when": "{{!exists('heartlib')}}",
            "method": "shell.run",
            "params": {
                "message": "git clone https://github.com/HeartMuLa/heartlib.git"
            }
        },
        {
            method: "shell.run",
            params: {
                venv: "env",
                message: "uv pip install -e ./heartlib"
            }
        },
        {
            method: "script.start",
            params: {
                uri: "torch.js",
                params: {
                    venv: "env",
                    path: "app",
                    flashattention: true,
                    xformers: true,
                    triton: true,
                    sageattention: true
                }
            }
        },
        {
            method: "hf.download",
            params: {
                local_dir: "ckpt",
                models: [
                    "HeartMuLa/HeartMuLaGen",
                    "HeartMuLa/HeartMuLa-oss-3B",
                    "HeartMuLa/HeartCodec-oss"
                ]
            }
        }
    ]
}
