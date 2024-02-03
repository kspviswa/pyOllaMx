![](assets/icon.png)
# PyOllaMx
#### `Your gateway to both Ollama & Apple MlX models`

Inspired by [Ollama](https://github.com/ollama/ollama), [Apple MlX](https://github.com/ml-explore/mlx) projects and frustrated by the dependencies from external applications like Bing, Chat-GPT etc, I wanted to have my own personal chatbot as a native MacOS application. Sure there are alternatives like streamlit, gradio (which are based, thereby needing a browser) or others like Ollamac, LMStudio, mindmac etc which are good but then restrictive in some means (either by license, or paid or not versatile). Also I wanted to enjoy both Ollama (based on `llama.cpp`) and Mlx models (which are suitable for image generation, audio generation etc and heck I own a mac with Apple silicon 👨🏻‍💻) through a single uniform interface.

All these lead to this project (PyOllaMx) and another sister project called [PyOMlx](https://github.com/kspviswa/PyOMlx).

I'm using these in my day to day workflow and I intend to keep develop these for my use and benifit. If you find this valuable, feel free to use it and contribute to this project as well.

MacOS DMGs are available in Releases

## PyOllaMx vs PyOMlx

[PyOllaMx](https://github.com/kspviswa/pyOllaMx) : ChatBot application capable of chatting with both Ollama and Apple MlX models. For this app to function, it needs both [Ollama](https://github.com/ollama/ollama) & [PyOMlx](https://github.com/kspviswa/PyOMlx) macos app running. These 2 apps will serve their respective models on localhost for PyOllaMx to chat.

[PyOMlx](https://github.com/kspviswa/PyOMlx) : A Macos App capable of discovering, loading & serving Apple MlX models downloaded from [Apple MLX Community repo in hugging face](https://huggingface.co/mlx-community) 🤗

## How to use?

1) Install [Ollama Application](https://ollama.ai/download) & use Ollama CLI to download your desired models
```
ollama pull <model name>
ollama pull mistral
```
This command will download the Ollama models in a known location to PyOllaMx

2) Install [MlX Models from Hugging Face repo](https://huggingface.co/mlx-community).

use hugging-face cli
```
pip install huggingface_hub hf_transfer

export HF_HUB_ENABLE_HF_TRANSFER=1
huggingface-cli download mlx-community/CodeLlama-7b-Python-4bit-MLX
```
This command will download the MlX models in a known location to PyOllaMx

3) Now simply open the **PyOllaMx** and start chatting

## v0.0.1 Features

- Auto discover Ollama & MlX models. Simply download the models as you do with respective tools and pyOllaMx would pull the models seamlessly
- Markdown support on chat messages for programming code
- Selectable Text
- Temperature control
