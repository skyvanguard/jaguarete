"""Chunk Manager Operator."""

from typing import List, Optional

from jaguarete.core import Chunk
from jaguarete.core.awel import MapOperator
from jaguarete.core.awel.flow import IOField, OperatorCategory, Parameter, ViewMetadata
from jaguarete.rag.knowledge.base import Knowledge
from jaguarete.util.i18n_utils import _
try:
    from jaguarete_ext.rag import ChunkParameters
    from jaguarete_ext.rag.chunk_manager import ChunkManager
except ImportError:
    ChunkParameters = None  # type: ignore[misc, assignment]
    ChunkManager = None  # type: ignore[misc, assignment]


class ChunkManagerOperator(MapOperator[Knowledge, List[Chunk]]):
    """Chunk Manager Operator."""

    metadata = ViewMetadata(
        label=_("Chunk Manager Operator"),
        name="chunk_manager_operator",
        description=_(" Split Knowledge Documents into chunks."),
        category=OperatorCategory.RAG,
        parameters=[
            Parameter.build_from(
                _("Chunk Split Parameters"),
                "chunk_parameters",
                ChunkParameters,
                description=_("Chunk Split Parameters."),
                optional=True,
                default=None,
                alias=["chunk_parameters"],
            ),
        ],
        inputs=[
            IOField.build_from(
                _("Knowledge"),
                "knowledge",
                Knowledge,
                description=_("The knowledge to be loaded."),
            )
        ],
        outputs=[
            IOField.build_from(
                _("Chunks"),
                "chunks",
                List[Chunk],
                description=_("The split chunks by chunk manager."),
                is_list=True,
            )
        ],
    )

    def __init__(
        self,
        chunk_parameters: Optional[ChunkParameters] = None,
        **kwargs,
    ):
        """Init the datasource operator."""
        MapOperator.__init__(self, **kwargs)
        self._chunk_parameters = chunk_parameters or ChunkParameters(
            chunk_strategy="Automatic"
        )

    async def map(self, knowledge: Knowledge) -> List[Chunk]:
        """Persist chunks in vector db."""
        documents = knowledge.load()
        chunk_manager = ChunkManager(
            knowledge=knowledge, chunk_parameter=self._chunk_parameters
        )
        return chunk_manager.split(documents)
