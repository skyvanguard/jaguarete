"""Tests for NVD CVE knowledge source."""


def test_nvd_load_documents():
    from jaguarete_knowledge.sources.nvd_cve import NvdCveSource
    source = NvdCveSource()
    docs = source.load_documents()
    assert len(docs) > 0
    assert "CVE-" in docs[0].content


def test_nvd_load_chunks():
    from jaguarete_knowledge.sources.nvd_cve import NvdCveSource
    source = NvdCveSource()
    chunks = source.load_chunks()
    assert len(chunks) > 0
    assert chunks[0].metadata.get("cve_id") is not None


def test_nvd_search_by_severity():
    from jaguarete_knowledge.sources.nvd_cve import NvdCveSource
    source = NvdCveSource()
    critical = source.search_by_severity(min_cvss=9.0)
    assert len(critical) > 0
    assert all(c["cvss"] >= 9.0 for c in critical)


def test_nvd_search_by_keyword():
    from jaguarete_knowledge.sources.nvd_cve import NvdCveSource
    source = NvdCveSource()
    results = source.search("Log4j")
    assert len(results) > 0


def test_nvd_metadata():
    from jaguarete_knowledge.sources.nvd_cve import NvdCveSource
    source = NvdCveSource()
    docs = source.load_documents()
    for doc in docs:
        assert "cvss" in doc.metadata
        assert "severity" in doc.metadata
