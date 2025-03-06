from presidio_analyzer import RecognizerRegistry

from constants import LANGUAGE

class Identifier:
    def __init__(self):
        self.registry = RecognizerRegistry()
        self.registry.load_predefined_recognizers()

    def get_all_identifiers(self):
        recognizers = self.registry.get_recognizers(language=LANGUAGE, all_fields=True)
        supported_entities = set()
        for recognizer in recognizers:
            supported_entities.update(recognizer.supported_entities)
        return list(supported_entities)

    def get_identifier_details(self, identifier_name):
        recognizers = self.registry.get_recognizers(language=LANGUAGE, all_fields=True)
        details = []
        for recognizer in recognizers:
            if identifier_name in recognizer.supported_entities:
                detail = {
                    'name': recognizer.name,
                    'supported_entities': recognizer.supported_entities,
                    'version': getattr(recognizer, 'version', 'N/A'),
                    'supported_language': getattr(recognizer, 'supported_language', 'N/A'),
                    'description': recognizer.__class__.__doc__.strip() if recognizer.__class__.__doc__ else 'No description available.'
                }
                details.append(detail)
        return details