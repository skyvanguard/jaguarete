"""Proxy models."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jaguarete.model.proxy.llms.chatgpt import OpenAILLMClient
    from jaguarete.model.proxy.llms.claude import ClaudeLLMClient
    from jaguarete.model.proxy.llms.ollama import OllamaLLMClient


def __lazy_import(name):
    module_path = {
        "OpenAILLMClient": "jaguarete.model.proxy.llms.chatgpt",
        "ClaudeLLMClient": "jaguarete.model.proxy.llms.claude",
        "OllamaLLMClient": "jaguarete.model.proxy.llms.ollama",
    }

    if name in module_path:
        module = __import__(module_path[name], fromlist=[name])
        return getattr(module, name)
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")


def __getattr__(name):
    return __lazy_import(name)


__all__ = [
    "OpenAILLMClient",
    "ClaudeLLMClient",
    "OllamaLLMClient",
]
