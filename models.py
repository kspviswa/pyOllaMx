import os
from pathlib import Path
from typing_extensions import List
import flet as ft
import re

DEFAULT_OLLAMA_MODEL_REGISTRY = Path("~/.ollama/models/manifests/registry.ollama.ai/library").expanduser()
DEFAULT_HF_MLX_MODEL_REGISTRY = Path("~/.cache/huggingface/hub/").expanduser()

def returnModels() -> List[str]:
    print(DEFAULT_OLLAMA_MODEL_REGISTRY)
    models = []
    for d in os.listdir(DEFAULT_OLLAMA_MODEL_REGISTRY):
        a_dir = os.path.join(DEFAULT_OLLAMA_MODEL_REGISTRY, d)
        if os.path.isdir(a_dir):
            for f in os.listdir(a_dir):
                if os.path.isfile(os.path.join(a_dir, f)):
                    model = f'{d}:{f}'
                    models.append(model)
    return models

def returnMlxModels() -> List[str]:
    print(DEFAULT_HF_MLX_MODEL_REGISTRY)
    models = []
    for d in os.listdir(DEFAULT_HF_MLX_MODEL_REGISTRY):
        a_dir = os.path.join(DEFAULT_HF_MLX_MODEL_REGISTRY, d)
        if os.path.isdir(a_dir) and not d.startswith('.'):
            print(f'a_dir is {a_dir}')
            model = re.split('--', d)[-1]  
            models.append(model)
    print(models)
    return models

def retModelOptions(isMlx=False):
    options = []
    for m in returnMlxModels() if isMlx else returnModels():
        options.append(ft.dropdown.Option(m))
    return options