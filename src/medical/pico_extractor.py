"""
OpenMedAgent - PICO Extraction Engine
Rule-based extraction of clinical research questions.
"""

import re


class PICOExtractor:

    def extract(self, question):

        if not question or not question.strip():
            raise ValueError("Research question cannot be empty.")

        text = question.strip()

        return {
            "population": self.extract_population(text),
            "intervention": self.extract_intervention(text),
            "comparison": self.extract_comparison(text),
            "outcome": self.extract_outcome(text),
            "original_question": text,
        }

    def extract_population(self, text):

        patterns = [
            r"in patients with ([^,?]+)",
            r"among patients with ([^,?]+)",
            r"in adults with ([^,?]+)",
            r"in children with ([^,?]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.I)

            if match:
                return match.group(1).strip()

        return None

    def extract_intervention(self, text):

        patterns = [
            r"effect of (.+?) compared with",
            r"impact of (.+?) compared with",
            r"effect of (.+?) versus",
            r"effect of (.+?) vs\.?",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.I)

            if match:
                return match.group(1).strip()

        return None

    def extract_comparison(self, text):

        patterns = [
            r"compared with (.+?)(?: on | in | for |\?|$)",
            r"versus (.+?)(?: on | in | for |\?|$)",
            r"vs\.? (.+?)(?: on | in | for |\?|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.I)

            if match:
                return match.group(1).strip()

        return None

    def extract_outcome(self, text):

        patterns = [
            r"on (?:the )?(.+?)\??$",
            r"effect on (.+?)\??$",
            r"impact on (.+?)\??$",
            r"reduction in (.+?)\??$",
            r"improvement in (.+?)\??$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.I)

            if match:
                return match.group(1).strip()

        return None