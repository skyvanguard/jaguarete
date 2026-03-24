"""Tests for OWASP knowledge source."""


def test_owasp_load_documents():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    docs = source.load_documents()
    assert len(docs) == 10  # OWASP Top 10


def test_owasp_load_chunks():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    chunks = source.load_chunks()
    assert len(chunks) == 10


def test_owasp_search():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    results = source.search("injection")
    assert len(results) > 0
    assert any("Injection" in r["name"] for r in results)


def test_owasp_get_by_id():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    entry = source.get_by_id("A01")
    assert entry is not None
    assert entry["name"] == "Broken Access Control"


def test_owasp_has_prevention():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    docs = source.load_documents()
    for doc in docs:
        assert "Prevention:" in doc.content


def test_owasp_metadata():
    from jaguarete_knowledge.sources.owasp import OwaspSource
    source = OwaspSource()
    docs = source.load_documents()
    for doc in docs:
        assert doc.metadata.get("source") == "owasp_top10"
        assert doc.metadata.get("owasp_id") is not None
