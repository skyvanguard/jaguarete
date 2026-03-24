"""NVD CVE knowledge source for RAG pipeline."""
from dataclasses import dataclass, field
from typing import Optional

from jaguarete.core.interface.knowledge import Chunk, Document


# Sample CVE entries for offline use
SAMPLE_CVES = [
    {
        "id": "CVE-2024-3094",
        "description": "Malicious code was discovered in the upstream tarballs of xz-utils, starting with version 5.6.0. The backdoor allows remote code execution via SSH.",
        "cvss": 10.0,
        "severity": "CRITICAL",
        "published": "2024-03-29",
        "affected": "xz-utils 5.6.0, 5.6.1",
        "vector": "NETWORK",
    },
    {
        "id": "CVE-2024-21762",
        "description": "A out-of-bounds write vulnerability in Fortinet FortiOS allows remote unauthenticated attackers to execute arbitrary code via specially crafted HTTP requests.",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "published": "2024-02-09",
        "affected": "FortiOS 7.4.0-7.4.2, 7.2.0-7.2.6",
        "vector": "NETWORK",
    },
    {
        "id": "CVE-2023-44228",
        "description": "Apache Log4j2 Remote Code Execution vulnerability allows attackers to execute arbitrary code via JNDI lookup in log messages.",
        "cvss": 10.0,
        "severity": "CRITICAL",
        "published": "2021-12-10",
        "affected": "Apache Log4j2 2.0-beta9 to 2.14.1",
        "vector": "NETWORK",
    },
    {
        "id": "CVE-2024-23897",
        "description": "Jenkins CLI arbitrary file read vulnerability allows unauthenticated attackers to read arbitrary files on the Jenkins controller file system.",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "published": "2024-01-24",
        "affected": "Jenkins <= 2.441, LTS <= 2.426.2",
        "vector": "NETWORK",
    },
    {
        "id": "CVE-2024-1709",
        "description": "ConnectWise ScreenConnect authentication bypass vulnerability allows unauthorized access to the setup wizard, enabling administrative account creation.",
        "cvss": 10.0,
        "severity": "CRITICAL",
        "published": "2024-02-19",
        "affected": "ConnectWise ScreenConnect <= 23.9.7",
        "vector": "NETWORK",
    },
]


@dataclass
class NvdCveSource:
    """NVD CVE knowledge source for RAG pipeline.

    Provides vulnerability descriptions, CVSS scores, and affected products
    as documents for vector embedding and retrieval.
    """

    name: str = "nvd_cve"
    description: str = "National Vulnerability Database CVE entries with CVSS scores"
    _cves: list = field(default_factory=lambda: SAMPLE_CVES)

    def load_documents(self) -> list[Document]:
        """Load CVE entries as documents for RAG indexing."""
        documents = []
        for cve in self._cves:
            content = self._format_cve(cve)
            doc = Document(
                content=content,
                metadata={
                    "source": "nvd_cve",
                    "cve_id": cve["id"],
                    "cvss": cve["cvss"],
                    "severity": cve["severity"],
                    "published": cve["published"],
                },
            )
            documents.append(doc)
        return documents

    def load_chunks(self) -> list[Chunk]:
        """Load CVE entries as pre-chunked items."""
        chunks = []
        for cve in self._cves:
            content = self._format_cve(cve)
            chunk = Chunk(
                content=content,
                metadata={
                    "source": "nvd_cve",
                    "cve_id": cve["id"],
                    "cvss": cve["cvss"],
                    "severity": cve["severity"],
                },
            )
            chunks.append(chunk)
        return chunks

    def search_by_severity(self, min_cvss: float = 7.0) -> list[dict]:
        """Search CVEs by minimum CVSS score."""
        return [c for c in self._cves if c["cvss"] >= min_cvss]

    def search(self, query: str) -> list[dict]:
        """Search CVEs by keyword."""
        query_lower = query.lower()
        return [
            c for c in self._cves
            if query_lower in c["description"].lower()
            or query_lower in c["id"].lower()
            or query_lower in c.get("affected", "").lower()
        ]

    async def fetch_latest(self, keyword: str = "", results_per_page: int = 20) -> bool:
        """Fetch latest CVEs from NVD API.

        Returns True if successfully updated.
        """
        import httpx

        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {"resultsPerPage": results_per_page}
        if keyword:
            params["keywordSearch"] = keyword

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            cves = []
            for vuln in data.get("vulnerabilities", []):
                cve_data = vuln.get("cve", {})
                cve_id = cve_data.get("id", "")

                description = ""
                for desc in cve_data.get("descriptions", []):
                    if desc.get("lang") == "en":
                        description = desc.get("value", "")
                        break

                cvss = 0.0
                severity = "UNKNOWN"
                metrics = cve_data.get("metrics", {})
                for version in ["cvssMetricV31", "cvssMetricV30"]:
                    if version in metrics:
                        cvss_data = metrics[version][0].get("cvssData", {})
                        cvss = cvss_data.get("baseScore", 0.0)
                        severity = cvss_data.get("baseSeverity", "UNKNOWN")
                        break

                cves.append({
                    "id": cve_id,
                    "description": description,
                    "cvss": cvss,
                    "severity": severity,
                    "published": cve_data.get("published", "")[:10],
                    "affected": "",
                    "vector": "NETWORK",
                })

            if cves:
                self._cves = cves
                return True
        except Exception:
            pass
        return False

    def _format_cve(self, cve: dict) -> str:
        """Format a CVE as readable text."""
        return (
            f"CVE: {cve['id']}\n"
            f"Severity: {cve['severity']} (CVSS: {cve['cvss']})\n"
            f"Published: {cve['published']}\n"
            f"Affected: {cve.get('affected', 'N/A')}\n"
            f"Attack Vector: {cve.get('vector', 'N/A')}\n"
            f"\nDescription:\n{cve['description']}"
        )
