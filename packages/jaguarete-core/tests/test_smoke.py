"""Smoke tests to verify jaguarete-core imports work after rename."""


def test_import_jaguarete():
    """Core package imports without errors."""
    import jaguarete
    assert jaguarete is not None


def test_import_agent_core():
    """Agent framework core classes are importable."""
    from jaguarete.agent.core.base_agent import ConversableAgent
    from jaguarete.agent.core.agent import Agent
    from jaguarete.agent.core.agent_manage import AgentManager
    assert ConversableAgent is not None
    assert Agent is not None
    assert AgentManager is not None


def test_import_agent_middleware():
    """Agent middleware system is importable."""
    from jaguarete.agent.middleware.base import AgentMiddleware
    assert AgentMiddleware is not None


def test_import_agent_resource():
    """Agent resource/tool system is importable."""
    from jaguarete.agent.resource.base import Resource, ResourceType
    from jaguarete.agent.resource.tool.base import tool
    assert Resource is not None
    assert ResourceType is not None
    assert tool is not None


def test_import_core_interfaces():
    """Core interfaces (LLM, embeddings, storage) are importable."""
    from jaguarete.core.interface.llm import LLMClient, ModelRequest, ModelOutput
    from jaguarete.core.interface.embeddings import Embeddings
    from jaguarete.core.interface.storage import StorageInterface
    assert LLMClient is not None
    assert ModelRequest is not None
    assert Embeddings is not None


def test_import_awel():
    """AWEL DAG system is importable."""
    from jaguarete.core.awel.dag.base import DAG
    from jaguarete.core.awel.operators.common_operator import MapOperator
    assert DAG is not None
    assert MapOperator is not None


def test_import_rag():
    """RAG pipeline components are importable."""
    from jaguarete.rag.text_splitter.text_splitter import RecursiveCharacterTextSplitter
    assert RecursiveCharacterTextSplitter is not None


def test_import_storage():
    """Storage layer is importable."""
    from jaguarete.storage.vector_store.base import VectorStoreBase
    assert VectorStoreBase is not None


def test_import_llm_openai():
    """OpenAI LLM adapter is importable."""
    from jaguarete.model.proxy.llms.chatgpt import OpenAILLMClient
    assert OpenAILLMClient is not None


def test_import_llm_claude():
    """Claude LLM adapter is importable."""
    from jaguarete.model.proxy.llms.claude import ClaudeLLMClient
    assert ClaudeLLMClient is not None


def test_import_llm_ollama():
    """Ollama LLM adapter is importable."""
    from jaguarete.model.proxy.llms.ollama import OllamaLLMClient
    assert OllamaLLMClient is not None
