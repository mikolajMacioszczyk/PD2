import os
import sys

configuration_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'configuration'))
sys.path.append(configuration_path)

import configuration

FHIR_SERVER = configuration.FHIR_SERVER
VERBOSE = configuration.VERBOSE