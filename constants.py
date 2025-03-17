import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MIN_API_ID = 1
MAX_API_ID = 999999999999999

REQUEST_METHODS_MAPPING = {
    '_get': 'GET',
    '_post': 'POST',
    '_put': 'PUT',
    '_delete': 'DELETE'
}  # keeps semanthic method by callable request method name
