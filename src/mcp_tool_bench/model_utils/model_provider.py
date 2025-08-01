import json
from typing import Dict, Any, Optional

from ..global_variables import *
from .qwen_api import QwenModelAPIProvider

_global_model_provider: Dict[str, Any] = {}

_global_model_provider[MODEL_SELECTION_QWEN3_PLUS] = QwenModelAPIProvider("qwen-plus")
_global_model_provider[MODEL_SELECTION_QWEN3_MAX] = QwenModelAPIProvider("qwen-max")
_global_model_provider[MODEL_SELECTION_QWEN3_CODER] = QwenModelAPIProvider("qwen3-coder-plus")
