from typing import Any, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

import requests
import json

class MlxLLM(LLM):
    llmHost = 'http://127.0.0.1:5000/serve'
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
        data = {'model': self.model, 'prompt': prompt, 'temp' : self.temp}
        response = requests.post(self.llmHost, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        return response.text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"llmHost": self.llmHost, "model":self.model, "temp" : self.temp}