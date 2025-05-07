import os
import sys

configuration_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(configuration_path)

import configuration

OPENEHR_SERVER = configuration.OPENEHR_SERVER
VERBOSE = configuration.VERBOSE
DATA_DIRECTORY_PATH = "../../data/"