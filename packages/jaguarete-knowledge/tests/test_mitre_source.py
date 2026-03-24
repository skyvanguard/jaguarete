"""Tests for MITRE ATT&CK knowledge source."""


def test_mitre_load_documents():
    from jaguarete_knowledge.sources.mitre_attack import MitreAttackSource
    source = MitreAttackSource()
    docs = source.load_documents()
    assert len(docs) > 0
    assert docs[0].content is not None
    assert "mitre_attack" in docs[0].metadata.get("source", "")


def test_mitre_load_chunks():
    from jaguarete_knowledge.sources.mitre_attack import MitreAttackSource
    source = MitreAttackSource()
    chunks = source.load_chunks()
    assert len(chunks) > 0
    assert chunks[0].metadata.get("technique_id") is not None


def test_mitre_search():
    from jaguarete_knowledge.sources.mitre_attack import MitreAttackSource
    source = MitreAttackSource()
    results = source.search("phishing")
    assert len(results) > 0
    assert any("Phishing" in r["name"] for r in results)


def test_mitre_get_by_tactic():
    from jaguarete_knowledge.sources.mitre_attack import MitreAttackSource
    source = MitreAttackSource()
    results = source.get_by_tactic("Initial Access")
    assert len(results) > 0
    assert all(r["tactic"] == "Initial Access" for r in results)


def test_mitre_technique_format():
    from jaguarete_knowledge.sources.mitre_attack import MitreAttackSource
    source = MitreAttackSource()
    docs = source.load_documents()
    for doc in docs:
        assert "MITRE ATT&CK Technique:" in doc.content
        assert "Tactic:" in doc.content
