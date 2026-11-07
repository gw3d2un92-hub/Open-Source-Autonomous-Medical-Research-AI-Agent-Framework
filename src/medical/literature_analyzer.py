"""
OpenMedAgent - Medical Literature Analyzer
Rule-based extraction from scientific abstracts.
"""

import re


class LiteratureAnalyzer:

    def analyze(self, publication):

        title = publication.get("title", "")
        abstract = publication.get("abstract", "")
        text = abstract.lower()

        return {
            "pmid": publication.get("pmid"),
            "title": title,
            "study_design": self.extract_study_design(text),
            "sample_size": self.extract_sample_size(text),
            "population": self.extract_population(text),
            "intervention": self.extract_intervention(text),
            "outcomes": self.extract_outcomes(text),
            "limitations": self.extract_limitations(text),
            "source": publication.get("url"),
        }

    def extract_study_design(self, text):

        designs = [
            "randomized controlled trial",
            "systematic review and meta-analysis",
            "systematic review",
            "meta-analysis",
            "prospective cohort study",
            "retrospective cohort study",
            "case-control study",
            "cross-sectional study",
            "observational study",
            "case series",
            "case report",
        ]

        for design in designs:
            if design in text:
                return design.title()

        return "Not identified"

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

    def extract_population(self, text):

        match = re.search(
            r"(?:patients|adults|children|participants) with [^.]{1,100}",
            text,
            re.I,
        )

        return match.group(0) if match else "Not identified"

    def extract_intervention(self, text):

        keywords = [
            "treated with",
            "received",
            "administered",
            "intervention",
        ]

        for keyword in keywords:
            if keyword in text:
                position = text.find(keyword)
                return text[position:position + 150]

        return "Not identified"

    def extract_outcomes(self, text):

        keywords = [
            "primary outcome",
            "primary endpoint",
            "mortality",
            "hospitalization",
            "clinical outcomes",
        ]

        return [
            keyword for keyword in keywords
            if keyword in text
        ]

    def extract_limitations(self, text):

        keywords = [
            "limitations",
            "small sample size",
            "selection bias",
            "short follow-up",
            "single-center",
        ]

        return [
            keyword for keyword in keywords
            if keyword in text
        ]