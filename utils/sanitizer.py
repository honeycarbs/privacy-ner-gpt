from re import findall

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class Sanitizer:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    """
        total_score = 100% * (1 - total PII / total prompt word count)
    """
    def calculate_privacy_score(self, prompt, detected_entities):
        words = findall(r'\b\w+\b', prompt)
        word_count = len(words)
        if word_count == 0:
            return 100 

        pii_word_ranges = set()

        for entity in detected_entities:
            entity_text = prompt[entity['start']:entity['end']]
            words_in_entity = findall(r'\b\w+\b', entity_text)
            for word in words_in_entity:
                pii_word_ranges.add(word)

        pii_word_count = len(pii_word_ranges)
        privacy_score = 100 * (1 - (pii_word_count / word_count))

        return round(privacy_score, 2)


    def sanitize_prompt(self, prompt: str):
        analyzer_results = self.analyzer.analyze(
            text=prompt,
            language='en'
        )

        anonymized_result = self.anonymizer.anonymize(
            text=prompt,
            analyzer_results=analyzer_results,
            operators={"DEFAULT": OperatorConfig("replace", {"new_value": "[REDACTED]"})}
        )

        detected_entities = [
            {
                "entity_type": result.entity_type,
                "start": result.start,
                "end": result.end,
                "score": result.score
            }
            for result in analyzer_results
        ]

        privacy_score = self.calculate_privacy_score(prompt, detected_entities)

        return {
            "sanitized_prompt": anonymized_result.text,
            "privacy_score": privacy_score,
            "detected_private_info": detected_entities
        }
