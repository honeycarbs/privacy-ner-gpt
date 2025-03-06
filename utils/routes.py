from flask import request, jsonify
from flask_restx import Namespace, Resource

from utils.sanitizer import Sanitizer
from utils.identifiers import Identifier

# Initialize IdentifierChecker
sanitizer = Sanitizer()
identifier = Identifier()


sanitize_ns = Namespace('sanitize', description='Sanitizes user prompts')
@sanitize_ns.route('/')
class SanitizeResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'prompt' not in data:
            return {'error': "Missing 'prompt' field"}, 400

        result = sanitizer.sanitize_prompt(data['prompt'])

        return result, 200
    

identifiers_ns = Namespace('identifiers', description='Handles identifiable private information')
@identifiers_ns.route('/')
class IdentifiersResource(Resource):
    def get(self):
        identifiers = identifier.get_all_identifiers()
        return jsonify(identifiers)

@identifiers_ns.route('/<string:identifier_name>')
class IdentifierDetailResource(Resource):
    def get(self, identifier_name):
        details = identifier.get_identifier_details(identifier_name)
        if not details:
            return {'message' : f'{identifier_name} is not supported in the current version of Presidio.'}, 200
        return jsonify(details)
    

healthcheck_ns = Namespace('healthcheck', description='API health check')

@healthcheck_ns.route('/')
class HealthCheck(Resource):
    def get(self):
        return {"status": "running"}, 200
    
