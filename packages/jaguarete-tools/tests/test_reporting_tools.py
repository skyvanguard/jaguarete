"""Tests for reporting tools."""


def test_report_builder_executive():
    from jaguarete_tools.reporting.report_builder import report_builder

    findings = (
        "critical:SQL injection in login form\n"
        "high:XSS in search\n"
        "low:Missing headers"
    )
    result = report_builder(
        "Test Report", findings, report_type="executive", target="web-app"
    )
    assert "Security Assessment Report" in result
    assert "CRITICAL" in result
    assert "web-app" in result


def test_report_builder_technical():
    from jaguarete_tools.reporting.report_builder import report_builder

    findings = "medium:Outdated TLS version"
    result = report_builder("TLS Audit", findings, report_type="technical")
    assert "Detailed Findings" in result
    assert "MEDIUM" in result


def test_risk_scorer_high_risk():
    from jaguarete_tools.reporting.risk_scorer import risk_scorer

    result = risk_scorer(
        attack_vector="network",
        attack_complexity="low",
        privileges_required="none",
        user_interaction="none",
        impact_confidentiality="high",
        impact_integrity="high",
        impact_availability="high",
    )
    assert "CRITICAL" in result or "HIGH" in result


def test_risk_scorer_low_risk():
    from jaguarete_tools.reporting.risk_scorer import risk_scorer

    result = risk_scorer(
        attack_vector="physical",
        attack_complexity="high",
        privileges_required="high",
        user_interaction="required",
        impact_confidentiality="low",
        impact_integrity="none",
        impact_availability="none",
    )
    assert "LOW" in result or "MEDIUM" in result


def test_secrets_scan_detects_aws_key():
    from jaguarete_tools.analysis.secrets_scan import secrets_scan

    code = 'aws_key = "AKIAIOSFODNN7EXAMPLE"'
    result = secrets_scan(code)
    assert "AWS Access Key" in result


def test_secrets_scan_detects_github_token():
    from jaguarete_tools.analysis.secrets_scan import secrets_scan

    code = "GITHUB_TOKEN=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef1234"
    result = secrets_scan(code)
    assert "GitHub Token" in result


def test_secrets_scan_clean_code():
    from jaguarete_tools.analysis.secrets_scan import secrets_scan

    code = 'x = 42\nprint("hello world")'
    result = secrets_scan(code)
    assert "No secrets detected" in result
