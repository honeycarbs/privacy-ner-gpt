import logging
import os

from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from config import Config
from constants import CONFIG_FILE_PATH, LOG_DIR, ANY_ORIGIN, EXPOSE_HEADERS
from exceptions import ServerException
from utils.flask import server_exception_handler, uncaught_exception_handler
from utils.routes import sanitize_ns, identifiers_ns, healthcheck_ns

cfg = Config(CONFIG_FILE_PATH)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

fh = logging.FileHandler(f"{LOG_DIR}/all.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

server = Flask(__name__)
server.url_map.strict_slashes = False
server.config.from_object(cfg)

CORS(server, resources={"*": ANY_ORIGIN}, expose_headers=EXPOSE_HEADERS)

api = Api(server, version='1.0', title='Santitzer API', prefix= '/api/v1', doc='/api/v1/doc', description='An API for prompt sanitizing platform using NER')


api.add_namespace(sanitize_ns, path="/sanitize")
api.add_namespace(identifiers_ns, path="/identifiers")
api.add_namespace(healthcheck_ns, path="/healthcheck")
    
server.errorhandler(ServerException)(server_exception_handler)

if not cfg.DEBUG:
    server.errorhandler(Exception)(uncaught_exception_handler)


if __name__ == '__main__':
    server.run(host="localhost", port=5000, debug=True)

