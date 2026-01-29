# [ARCHIVED] HeartMuLa (Pinokio App)

NOTE: This project has been archived as an alternative that will be better maintained has been released. Check out https://github.com/fspecii/HeartMuLa-Studio

A lightweight **Pinokio community wrapper** for **HeartMuLa / heartlib** that provides a one-click local setup and a simple **Gradio UI** for generating music conditioned on **lyrics** + optional **tags**.

This repo does **not** contain the model code or weights. During install it:
- clones `https://github.com/HeartMuLa/heartlib`
- installs it editable into a `python=3.10` environment
- downloads the official checkpoints into `./ckpt`
- launches `app.py` (Gradio) and saves outputs to `./outputs`

## Usage (Pinokio)
1. **Install** (downloads checkpoints — first run takes a while)
2. **Start**
3. Open the UI link shown by Pinokio
4. Paste lyrics (and tags if you want) → **Generate**
5. Your audio file appears in `./outputs`

## Notes
- Recommended: NVIDIA GPU + CUDA for speed (CPU works but is much slower).
- Tags are expected as **comma-separated without spaces** (matches HeartMuLa docs).
- If MP3 saving fails on some systems, use `.wav` output (more portable).

## Credits / Upstream
This is an **unofficial wrapper**. All credit for the model, code and research goes to the HeartMuLa authors and the `heartlib` project:

**HeartMuLa: A Family of Open Sourced Music Foundation Models** (arXiv:2601.10547)  
Hugging Face models:
- `HeartMuLa/HeartMuLaGen`
- `HeartMuLa/HeartMuLa-oss-3B`
- `HeartMuLa/HeartCodec-oss`

HeartMuLa’s upstream README also credits work based on ConversationTTS.

## License
HeartMuLa/heartlib is licensed under the
**Apache License 2.0**
A permissive license whose main conditions require preservation of copyright and license notices. 
Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
You are responsible for ensuring any generated content does not infringe third-party rights.

## Citation
```bibtex
@misc{yang2026heartmulafamilyopensourced,
      title={HeartMuLa: A Family of Open Sourced Music Foundation Models}, 
      author={Dongchao Yang and Yuxin Xie and Yuguo Yin and Zheyu Wang and Xiaoyu Yi and Gongxi Zhu and Xiaolong Weng and Zihan Xiong and Yingzhe Ma and Dading Cong and Jingliang Liu and Zihang Huang and Jinghan Ru and Rongjie Huang and Haoran Wan and Peixu Wang and Kuoxi Yu and Helin Wang and Liming Liang and Xianwei Zhuang and Yuanyuan Wang and Haohan Guo and Junjie Cao and Zeqian Ju and Songxiang Liu and Yuewen Cao and Heming Weng and Yuexian Zou},
      year={2026},
      eprint={2601.10547},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2601.10547}, 
}
