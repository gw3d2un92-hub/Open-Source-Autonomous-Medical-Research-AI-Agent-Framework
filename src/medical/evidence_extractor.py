"""
OpenMedAgent - Medical Evidence Extractor

Extracts quantitative statistical information
from scientific abstracts using rule-based methods.

Unverified findings must be checked against the original paper.
"""

import re


class EvidenceExtractor:

    def extract(self, publication):

        abstract = publication.get("abstract", "")

        return {
            "pmid": publication.get("pmid"),
            "title": publication.get("title"),
            "sample_size": self.extract_sample_size(abstract),
            "hazard_ratios": self.extract_hazard_ratios(abstract),
            "odds_ratios": self.extract_odds_ratios(abstract),
            "risk_ratios": self.extract_risk_ratios(abstract),
            "confidence_intervals": self.extract_confidence_intervals(abstract),
            "p_values": self.extract_p_values(abstract),
            "source": publication.get("url"),
            "verification_required": True,
        }

    def extract_sample_size(self, text):

        patterns = [
            r"\b(\d[\d,]*)\s+(?:patients|participants|subjects)\b",
            r"\bn\s*=\s*(\d[\d,]*)\b",
        ]

        for pattern in patterns:

            match = re.search(pattern, text, re.I)

            if match:
                return int(match.group(1).replace(",", ""))

        return None

    def extract_hazard_ratios(self, text):

        return self._extract_statistic(
            text,
            r"\bHR\s*[:=]?\s*([\d.]+)"
        )

    def extract_odds_ratios(self, text):

        return self._extract_statistic(
            text,
            r"\bOR\s*[:=]?\s*([\d.]+)"
        )

    def extract_risk_ratios(self, text):

        return self._extract_statistic(
            text,
            r"\bRR\s*[:=]?\s*([\d.]+)"
        )

    def extract_confidence_intervals(self, text):

        pattern = (
            r"(?:95%\s*)?CI\s*[:=]?\s*"
            r"[\[(]?\s*([\d.]+)\s*[-–,]\s*([\d.]+)"
        )

        return [
            {
                "lower": float(match.group(1)),
                "upper": float(match.group(2))
            }
            for match in re.finditer(pattern, text, re.I)
        ]

    def extract_p_values(self, text):
        pattern = r"\bP\s*[=<]\s*(0?\.\d+|1(?:\.0+)?)\b"

        return [
            float(match.group(1))
            for match in re.finditer(pattern, text, re.I)
        ]

    def _extract_statistic(self, text, pattern):

        return [
            float(match.group(1))
            for match in re.finditer(pattern, text, re.I)
        ]
