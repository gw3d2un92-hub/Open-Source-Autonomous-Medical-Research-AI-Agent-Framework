"""
OpenMedAgent - PubMed Research Client

Searches PubMed and retrieves scientific publications
using the NCBI E-utilities API.
"""

import os
import requests
import xml.etree.ElementTree as ET

from typing import Optional


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


class PubMedClient:

    def __init__(self, email: Optional[str] = None):

        self.email = email or os.getenv("NCBI_EMAIL")

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "OpenMedAgent/0.1"
        })

    def search(self, query: str, max_results: int = 10):

        """
        Search PubMed for scientific publications.
        """

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
        }

        if self.email:
            params["email"] = self.email

        response = self.session.get(
            BASE_URL + "esearch.fcgi",
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data["esearchresult"]["idlist"]

    def fetch_details(self, pmids: list[str]):

        """
        Retrieve publication details using PubMed IDs.
        """

        if not pmids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        }

        if self.email:
            params["email"] = self.email

        response = self.session.get(
            BASE_URL + "efetch.fcgi",
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)

        publications = []

        for article in root.findall(".//PubmedArticle"):

            medline = article.find("MedlineCitation")
            article_data = medline.find("Article")

            pmid = medline.findtext("PMID", default="")

            title_element = article_data.find("ArticleTitle")

            title = (
                "".join(title_element.itertext())
                if title_element is not None
                else "Title unavailable"
            )

            abstract_parts = []

            for item in article_data.findall(
                "Abstract/AbstractText"
            ):
                text = "".join(item.itertext())
                label = item.attrib.get("Label")

                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)

            abstract = "\n".join(abstract_parts)

            journal = article_data.findtext(
                "Journal/Title",
                default="",
            )

            authors = []

            for author in article_data.findall(
                "AuthorList/Author"
            ):

                last = author.findtext("LastName", default="")
                fore = author.findtext("ForeName", default="")

                name = f"{fore} {last}".strip()

                if name:
                    authors.append(name)

            publications.append({

                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "authors": authors,

                "source": "PubMed",

                "url": (
                    f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                ),

            })

        return publications

    def search_and_fetch(
        self,
        query: str,
        max_results: int = 10,
    ):

        """
        Search PubMed and retrieve complete available records.
        """

        pmids = self.search(
            query=query,
            max_results=max_results,
        )

        return self.fetch_details(pmids)
