import json
from typing import Dict, Any, Optional

from ..global_variables import *
from .qwen_api import QwenModelAPIProvider
from .kimi_api import KimiModelAPIProvider
from .claude_api import ClaudeModelAPIProvider
from .openai_api import OpenAIModelAPIProvider

_global_model_provider: Dict[str, Any] = {}

## CLAUDE
_global_model_provider[MODEL_SELECTION_CLAUDE_37] = ClaudeModelAPIProvider(MODEL_SELECTION_CLAUDE_37)
_global_model_provider[MODEL_SELECTION_CLAUDE_OPUS_4] = ClaudeModelAPIProvider(MODEL_SELECTION_CLAUDE_OPUS_4)
## OPENAI
_global_model_provider[MODEL_SELECTION_GPT4O] = OpenAIModelAPIProvider(MODEL_SELECTION_GPT4O)
## QWEN
_global_model_provider[MODEL_SELECTION_QWEN25_MAX] = QwenModelAPIProvider(MODEL_SELECTION_QWEN25_MAX)
_global_model_provider[MODEL_SELECTION_QWEN3_PLUS] = QwenModelAPIProvider(MODEL_SELECTION_QWEN3_PLUS)
_global_model_provider[MODEL_SELECTION_QWEN3_TURBO] = QwenModelAPIProvider(MODEL_SELECTION_QWEN3_TURBO)
_global_model_provider[MODEL_SELECTION_QWEN3_235B] = QwenModelAPIProvider(MODEL_SELECTION_QWEN3_235B)
_global_model_provider[MODEL_SELECTION_QWEN3_CODER] = QwenModelAPIProvider(MODEL_SELECTION_QWEN3_CODER)

## KIMI
_global_model_provider[MODEL_SELECTION_KIMI_K2] = KimiModelAPIProvider(MODEL_SELECTION_KIMI_K2)
