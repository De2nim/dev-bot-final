import requests
import json
from urllib.parse import urlparse, parse_qs
from langchain_core.tools import tool
from pydantic.color import parse_str
# from ui import  unit_test_response




def get_files_list(BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME) :
    file_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/files?at=refs/heads/{BRANCH}"
    file_response = requests.get(file_url, auth=(USERNAME, ACCESS_TOKEN))

    if file_response.status_code != 200:
        print("Failed to fetch the files, Error Code : " + file_response.status_code)

    file_response.raise_for_status()
    file_list_json =  file_response.json()['values']
    # print(file_list_json)
    return file_list_json






def get_repo(FILE_PATH, BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME) :
    # FILE_PATH = 'run_code.py'
    repo_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/browse/{FILE_PATH}?at=refs/heads/{BRANCH}"
    # repo_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/browse"
    repo_response = requests.get(repo_url, auth=(USERNAME, ACCESS_TOKEN))
    repo_response.raise_for_status()
    repo_data = repo_response.json()
    print(repo_data)
    return repo_response.text


# get_repo()


@tool
def implementation():
    """
    The Particular function returns the json file which contains the all the code in the given branch in a
    given repository.Your work is to write the Unit Tests for code and provide the data for the same.
    also you have to convert the response in proper string such that it will explicitly show unit tests for each file.
    The response should be in MARKDOWN format.
    """
    with open('config.json', 'r') as file:
        config = json.load(file)

        BASE_URL = 'https://git.rakuten-it.com/rest/api/1.0'
        USERNAME = config['credentials_2']['username']
        ACCESS_TOKEN = config['credentials_2']['access_token']
        REPO_URL = config['credentials_2']['repo_url']

        parsed_url = urlparse(REPO_URL)
        path_components = parsed_url.path.split('/')
        REPO_OWNER = path_components[2]
        REPO_SLUG = path_components[4]
        # BRANCH  = 'code_review_agent'

        query_param = parse_qs(parsed_url.query)

        branch_ref = query_param.get('at', [None])[0]

        if branch_ref and branch_ref.startswith('refs/heads/'):
            BRANCH = branch_ref[len('refs/heads/'):]
        else:
            BRANCH = None
        # print("Repo Owner : " + REPO_OWNER + "\n" + "Repo Name : " + REPO_SLUG + "\n" + "Branch Name : " + BRANCH)

        file_list = get_files_list(BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME)
        print(file_list)
        # file_resp = get_repo()

        all_content = {}

        for FILE_PATH in file_list:
            content = get_repo(FILE_PATH,BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME)
            if content is not None:
                all_content[FILE_PATH] = content

        for FILE_PATH, content in all_content.items():
            print(f"Contents of {FILE_PATH} : \n {content}\n")

    return  all_content


# implementation()
#
# import requests
# import json
# from urllib.parse import urlparse, parse_qs
# from langchain_core.tools import tool
# from pydantic.color import parse_str
# # from ui import  unit_test_response
#
#
#
#
# def get_files_list(BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME) :
#     file_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/files?at=refs/heads/{BRANCH}"
#     file_response = requests.get(file_url, auth=(USERNAME, ACCESS_TOKEN))
#
#     if file_response.status_code != 200:
#         print("Failed to fetch the files, Error Code : " + file_response.status_code)
#
#     file_response.raise_for_status()
#     file_list_json =  file_response.json()['values']
#     return file_list_json
#
#
#
#
#
#
# def get_repo(FILE_PATH, BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME) :
#     # FILE_PATH = 'run_code.py'
#     repo_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/browse/{FILE_PATH}?at=refs/heads/{BRANCH}"
#     # repo_url = f"{BASE_URL}/projects/{REPO_OWNER}/repos/{REPO_SLUG}/browse"
#     repo_response = requests.get(repo_url, auth=(USERNAME, ACCESS_TOKEN))
#     repo_response.raise_for_status()
#     repo_data = repo_response.json()
#     print(repo_data)
#     return repo_response.text
#
#
# # get_repo()
#
#
# @tool
# def implementation():
#     """
#     The Particular function returns the json file which contains the all the code in the given branch in a
#     given repository.Your work is to write the detailed Unit Tests for code and provide the data for the same.
#     also you have to convert the response in proper string such that it will explicitly show unit tests for each file.
#     The response should be in MARKDOWN format.
#     """
#     with open('config.json', 'r') as file:
#         config = json.load(file)
#
#         BASE_URL = 'https://git.rakuten-it.com/rest/api/1.0'
#         USERNAME = config['credentials_2']['username']
#         ACCESS_TOKEN = config['credentials_2']['access_token']
#         REPO_URL = config['credentials_2']['repo_url']
#
#         parsed_url = urlparse(REPO_URL)
#         path_components = parsed_url.path.split('/')
#         REPO_OWNER = path_components[2]
#         REPO_SLUG = path_components[4]
#         # BRANCH  = 'code_review_agent'
#
#         query_param = parse_qs(parsed_url.query)
#
#         branch_ref = query_param.get('at', [None])[0]
#
#         if branch_ref and branch_ref.startswith('refs/heads/'):
#             BRANCH = branch_ref[len('refs/heads/'):]
#         else:
#             BRANCH = None
#         # print("Repo Owner : " + REPO_OWNER + "\n" + "Repo Name : " + REPO_SLUG + "\n" + "Branch Name : " + BRANCH)
#
#         file_list = get_files_list(BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME)
#         print(file_list)
#         # file_resp = get_repo()
#
#         all_content = {}
#
#         for FILE_PATH in file_list:
#             content = get_repo(FILE_PATH,BASE_URL, REPO_OWNER, REPO_SLUG, BRANCH, ACCESS_TOKEN, USERNAME)
#             if content is not None:
#                 all_content[FILE_PATH] = content
#
#         for FILE_PATH, content in all_content.items():
#             print(f"Contents of {FILE_PATH} : \n {content}\n")
#
#     return  all_content
#
#
# # implementation()
#
#
