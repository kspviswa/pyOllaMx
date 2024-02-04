from typing import Any, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

import requests
import json

from mlx_lm import load, generate
import os
from pathlib import Path

DEFAULT_HF_MLX_MODEL_REGISTRY = Path("~/.cache/huggingface/hub/").expanduser()

class MlxLLM_local(LLM):
    model = ""
    temp = 0.3
    def __init__(self, model="", temp=0.3):
        super().__init__()
        self.model = model
        self.temp = temp


    @property
    def _llm_type(self) -> str:
        return "mlxLLM"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return self.firePrompt(prompt)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model":self.model, "temp" : self.temp}
    
    def firePrompt(self, prompt: str):
        model_dir = f'{DEFAULT_HF_MLX_MODEL_REGISTRY}/models--mlx-community--{self.model}'
        model_digest = ""
        with open(f'{model_dir}/refs/main', 'r') as f:
            model_digest = f.read()
        model_path = f'{model_dir}/snapshots/{model_digest}'
        model, tokenizer = load(model_path, {'trust_remote_code':True})
        response = generate(model, tokenizer, prompt=prompt, max_tokens=500, temp=self.temp)
        return response