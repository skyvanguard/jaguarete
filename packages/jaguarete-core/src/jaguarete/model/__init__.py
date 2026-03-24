from .adapter.auto_client import AutoLLMClient  # noqa: F401

__ALL__ = [
    "AutoLLMClient",
]

_HAS_SCAN = False


def scan_model_providers():
    """Scan and register all model providers."""
    from jaguarete.core.interface.parameter import (
        EmbeddingDeployModelParameters,
        LLMDeployModelParameters,
    )
    from jaguarete.util.module_utils import ModelScanner, ScannerConfig

    global _HAS_SCAN

    if _HAS_SCAN:
        return
    scanner = ModelScanner[LLMDeployModelParameters]()
    config = ScannerConfig(
        module_path="jaguarete.model.adapter",
        base_class=LLMDeployModelParameters,
        specific_files=[
            "vllm_adapter",
            "mlx_adapter",
            "hf_adapter",
            "llama_cpp_adapter",
            "llama_cpp_py_adapter",
        ],
    )
    config_llms = ScannerConfig(
        module_path="jaguarete.model.proxy.llms",
        base_class=LLMDeployModelParameters,
        recursive=True,
    )
    embedding_config = ScannerConfig(
        module_path="jaguarete.rag.embedding",
        base_class=EmbeddingDeployModelParameters,
        specific_files=["embeddings"],
    )
    reranker_config = ScannerConfig(
        module_path="jaguarete.rag.embedding",
        base_class=EmbeddingDeployModelParameters,
        specific_files=["rerank"],
    )
    scanner.scan_and_register(config)
    scanner.scan_and_register(config_llms)
    scanner.scan_and_register(embedding_config)
    scanner.scan_and_register(reranker_config)

    _HAS_SCAN = True
    return scanner.get_registered_items()
