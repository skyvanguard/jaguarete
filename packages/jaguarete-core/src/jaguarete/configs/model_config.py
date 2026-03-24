"""Model configuration shim.

Provides essential path constants and utility functions that were in the
original configs/model_config module. Values are resolved from environment
variables or sensible defaults.
"""

import os
from pathlib import Path


def resolve_root_path() -> str:
    """Resolve the project root path."""
    env_root = os.getenv("JAGUARETE_ROOT_PATH")
    if env_root:
        return env_root
    # Default: walk up from this file to find the project root
    return str(Path(__file__).resolve().parents[4])


ROOT_PATH = resolve_root_path()
PILOT_PATH = os.path.join(ROOT_PATH, "pilot")
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(ROOT_PATH, "models"))
DATA_DIR = os.getenv("DATA_DIR", os.path.join(ROOT_PATH, "data"))
LOGDIR = os.getenv("LOGDIR", os.path.join(ROOT_PATH, "logs"))
LOCALES_DIR = os.path.join(ROOT_PATH, "i18n", "locales")
SKILLS_DIR = os.getenv("SKILLS_DIR", os.path.join(ROOT_PATH, "skills"))
KNOWLEDGE_UPLOAD_ROOT_PATH = os.getenv(
    "KNOWLEDGE_UPLOAD_ROOT_PATH", os.path.join(ROOT_PATH, "data")
)

# LLM model configuration mapping (empty default -- populate as needed)
LLM_MODEL_CONFIG: dict = {}


def get_device() -> str:
    """Get the compute device to use."""
    import torch

    if torch.cuda.is_available():
        return "cuda"
    try:
        if torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"
