"""CVE lookup tool using the NVD API."""
import json

from jaguarete.agent.resource.tool.base import tool
from typing_extensions import Annotated, Doc


@tool(description="Look up CVE vulnerability details from the National Vulnerability Database")
async def cve_lookup(
    cve_id: Annotated[str, Doc("CVE identifier (e.g., CVE-2024-1234)")],
) -> str:
    """Query the NVD API for CVE vulnerability details.

    Returns CVE description, CVSS score, affected products, and references.
    """
    import httpx

    results = []
    results.append(f"CVE Lookup: {cve_id}")
    results.append("=" * 50)

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        vulns = data.get("vulnerabilities", [])
        if not vulns:
            return f"No results found for {cve_id}"

        cve = vulns[0].get("cve", {})

        # Description
        descriptions = cve.get("descriptions", [])
        for desc in descriptions:
            if desc.get("lang") == "en":
                results.append(f"\nDescription: {desc.get('value', 'N/A')}")
                break

        # CVSS Score
        metrics = cve.get("metrics", {})
        for version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            if version in metrics:
                cvss_data = metrics[version][0].get("cvssData", {})
                score = cvss_data.get("baseScore", "N/A")
                severity = cvss_data.get("baseSeverity", "N/A")
                results.append(f"CVSS Score: {score} ({severity})")
                results.append(
                    f"Attack Vector: {cvss_data.get('attackVector', 'N/A')}"
                )
                break

        # Published date
        published = cve.get("published", "N/A")
        results.append(f"Published: {published}")

        # References
        refs = cve.get("references", [])
        if refs:
            results.append("\nReferences:")
            for ref in refs[:5]:
                results.append(f"  - {ref.get('url', 'N/A')}")

    except httpx.HTTPError as e:
        results.append(f"NVD API error: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        results.append(f"Parse error: {e}")

    return "\n".join(results)
