import os
import time
from typing import List, Dict

import requests


EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NCBI_TOOL = "MedImpactAI"
NCBI_EMAIL = os.getenv("NCBI_EMAIL")
NCBI_API_KEY = os.getenv("NCBI_API_KEY")


class PubMedRetriever:
    def __init__(self, max_results: int = 5):
        if max_results < 1:
            raise ValueError("max_results must be at least 1")

        if not NCBI_EMAIL:
            raise ValueError(
                "NCBI_EMAIL environment variable is required."
            )

        self.max_results = max_results

    def _request(self, endpoint: str, params: Dict) -> requests.Response:
        params = {
            **params,
            "tool": NCBI_TOOL,
            "email": NCBI_EMAIL,
        }

        if NCBI_API_KEY:
            params["api_key"] = NCBI_API_KEY

        response = requests.get(
            f"{EUTILS_BASE_URL}/{endpoint}",
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        # Stay within NCBI's request-rate limits.
        time.sleep(0.35)

        return response

    def search(self, query: str) -> List[str]:
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        response = self._request(
            "esearch.fcgi",
            {
                "db": "pubmed",
                "term": query.strip(),
                "retmode": "json",
                "retmax": self.max_results,
            },
        )

        data = response.json()

        return data.get("esearchresult", {}).get("idlist", [])

    def fetch_metadata(self, pmids: List[str]) -> List[Dict]:
        if not pmids:
            return []

        response = self._request(
            "esummary.fcgi",
            {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "json",
            },
        )

        data = response.json()
        result = data.get("result", {})

        records = []

        for pmid in pmids:
            record = result.get(pmid)

            if not record:
                continue

            records.append(
                {
                    "pmid": pmid,
                    "title": record.get("title", ""),
                    "journal": record.get("fulljournalname", ""),
                    "publication_date": record.get("pubdate", ""),
                    "authors": [
                        author.get("name", "")
                        for author in record.get("authors", [])
                        if author.get("name")
                    ],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                }
            )

        return records

    def fetch_abstracts(self, pmids: List[str]) -> Dict[str, str]:
        if not pmids:
            return {}

        response = self._request(
            "efetch.fcgi",
            {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
            },
        )

        from xml.etree import ElementTree

        root = ElementTree.fromstring(response.text)

        abstracts = {}

        for article in root.findall(".//PubmedArticle"):
            pmid_element = article.find(".//PMID")

            if pmid_element is None:
                continue

            pmid = pmid_element.text

            abstract_parts = []

            for abstract_text in article.findall(".//AbstractText"):
                text = "".join(abstract_text.itertext()).strip()

                if text:
                    label = abstract_text.get("Label")

                    if label:
                        text = f"{label}: {text}"

                    abstract_parts.append(text)

            abstracts[pmid] = " ".join(abstract_parts)

        return abstracts

    def search_and_fetch(self, query: str) -> List[Dict]:
        pmids = self.search(query)

        records = self.fetch_metadata(pmids)
        abstracts = self.fetch_abstracts(pmids)

        for record in records:
            record["abstract"] = abstracts.get(
                record["pmid"],
                "",
            )

        return records


def main():
    print("=" * 60)
    print("MedImpact AI - PubMed Retriever")
    print("=" * 60)

    query = "HbA1c diabetes management"

    retriever = PubMedRetriever(max_results=5)

    records = retriever.search_and_fetch(query)

    print(f"\nQuery: {query}")
    print(f"\nRecords found: {len(records)}")

    for record in records:
        print("\n" + "-" * 60)

        print(f"PMID: {record['pmid']}")
        print(f"Title: {record['title']}")
        print(f"Journal: {record['journal']}")
        print(f"Publication date: {record['publication_date']}")
        print(f"URL: {record['url']}")

        abstract = record.get("abstract", "")

        if abstract:
            print("\nAbstract:")
            print(abstract[:1000])
        else:
            print("\nAbstract: Not available")


if __name__ == "__main__":
    main()

