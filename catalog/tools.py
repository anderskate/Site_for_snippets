from .models import Snippet
import re
import requests
import rfc6266_parser as rfc6266


def check_file_extension(file_name):
    extensions = []
    for i in Snippet.LANGUAGES:
        extensions.append(i[0])
    if not '.' in file_name:
        return False
    extension_file = file_name.split('.')[1]
    if extension_file in extensions:
        return True

    return False

def get_filename(response):
    header = response.headers
    content_type = header.get('content-type')

    if 'text/plain' in content_type.lower():
        filename = rfc6266.parse_requests_response(response).filename_unsafe
    else:
        filename = get_filename_from_cd(header.get('content-disposition'))

    return filename


def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall(r'".+"', cd)[0]
    formating_name = fname[1:-1]
    if len(fname) == 0:
        return None
    return formating_name


def get_data_by_link(link):
    try:
        response = requests.get(link, allow_redirects=True)
    except Exception:
        return False
    return response
