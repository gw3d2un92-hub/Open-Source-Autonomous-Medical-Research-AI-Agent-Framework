"""
OpenMedAgent - Integrated Medical Research Engine

Connects PICO extraction, PubMed searching,
and literature analysis.
"""

from src.medical.pico_extractor import PICOExtractor
from src.medical.pubmed_client import PubMedClient
from src.medical.literature_analyzer import LiteratureAnalyzer


class MedicalResearchEngine:

    def __init__(self):

        self.pico = PICOExtractor()
        self.pubmed = PubMedClient()
        self.analyzer = LiteratureAnalyzer()

    def generate_search_query(self, pico):

        population = pico.get("population") or ""
        intervention = pico.get("intervention") or ""
        comparison = pico.get("comparison") or ""
        outcome = pico.get("outcome") or ""

        terms = [
            population,
            intervention,
            comparison,
            outcome
        ]

        terms = [term for term in terms if term]

        return " AND ".join(
            f'"{term}"' for term in terms
        )

    def research(self, clinical_question, max_results=10):

        # Step 1: Extract PICO
        pico_data = self.pico.extract(clinical_question)

        # Step 2: Generate PubMed query
        search_query = self.generate_search_query(pico_data)

        # Step 3: Retrieve publications
        publications = self.pubmed.search_and_fetch(
            search_query,
            max_results
        )

        # Step 4: Analyze publications
        analyzed = [
            self.analyzer.analyze(paper)
            for paper in publications
        ]

        return {
            "clinical_question": clinical_question,
            "pico": pico_data,
            "search_query": search_query,
            "total_retrieved": len(publications),
            "publications": analyzed
        }