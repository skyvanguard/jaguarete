"""Tests for threat intelligence tools."""


def test_mitre_attack_map_by_id():
    from jaguarete_tools.intel.mitre_attack import mitre_attack_map

    result = mitre_attack_map(technique_id="T1190")
    assert "Exploit Public-Facing Application" in result
    assert "Initial Access" in result


def test_mitre_attack_map_by_keyword():
    from jaguarete_tools.intel.mitre_attack import mitre_attack_map

    result = mitre_attack_map(keyword="phishing")
    assert "T1566" in result


def test_mitre_attack_map_list_tactics():
    from jaguarete_tools.intel.mitre_attack import mitre_attack_map

    result = mitre_attack_map()
    assert "Available tactics" in result
    assert "Reconnaissance" in result


def test_cve_lookup_callable():
    from jaguarete_tools.intel.cve_lookup import cve_lookup

    assert callable(cve_lookup)
