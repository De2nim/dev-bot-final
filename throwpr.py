import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from langchain_core.tools import tool
from repofetch import implementation


now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

def create_branch(username, password, project_key, repo_slug, new_branch_name, source_branch_name):
    url = f"https://git.rakuten-it.com/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/branches"
    payload = {
        "name": new_branch_name,
        "startPoint": f"refs/heads/{source_branch_name}"
    }
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))
    if response.status_code == 201 or response.status_code == 200:
        print("Branch created successfully.\n")
        return True
    else:
        print(f"Failed to create branch: {response.status_code}")
        print(response.json())
        return False


def create_file_in_branch(username, password, project_key, repo_slug, branch_name, file_path, file_content):
    url = f"https://git.rakuten-it.com/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/browse/{file_path}?at=refs/heads/{branch_name}"

    data = MultipartEncoder(
        fields={
            # 'content': base64.b64encode(file_content.encode()).decode(),
            'content' : file_content,
            'message': f"Adding {file_path} to {branch_name}",
            'branch': branch_name
        }
    )
    headers = {
        'Content-Type': data.content_type
    }
    response = requests.put(url, data=data, headers=headers, auth=HTTPBasicAuth(username, password))
    if response.status_code == 201:
        print(f"File {file_path} created successfully in branch {branch_name}.")
    else:
        print(f"Failed to create file {file_path} in branch {branch_name}: {response.status_code}")
        try:
            print(response.json())
        except ValueError:
            print(response.text)


def create_pull_request(username, password, project_key, repo_slug, from_branch, to_branch, title, description):
    url = f"https://git.rakuten-it.com/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/pull-requests"
    payload = {
        "title": title,
        "description": description,
        "state": "OPEN",
        "open": True,
        "closed": False,
        "fromRef": {
            "id": f"refs/heads/{from_branch}",
            "repository": {
                "slug": repo_slug,
                "project": {
                    "key": project_key
                }
            }
        },
        "toRef": {
            "id": f"refs/heads/{to_branch}",
            "repository": {
                "slug": repo_slug,
                "project": {
                    "key": project_key
                }
            }
        },
        "locked": False,
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))
    if response.status_code == 201:
        print("Pull request created successfully.")
    else:
        print(f"Failed to create pull request: {response.status_code}")
        print(response.json())

    return  response.json()




def send_pr() :

    # prev_tool = implementation

    with open('config.json', 'r') as file:
        config = json.load(file)

    username = config['credentials_3']['username']
    password = config['credentials_3']['password']
    repo_url = config['credentials_3']['repo_url']

    parsed_url = urlparse(repo_url)
    path_components = parsed_url.path.split('/')

    project_key = path_components[2]
    repo_slug = path_components[4]

    query_param = parse_qs(parsed_url.query)
    branch_ref = query_param.get('at', [None])[0]
    if branch_ref and branch_ref.startswith('refs/heads/'):
        source_branch_name = branch_ref[len('refs/heads/'):]
    else:
        source_branch_name = None

    new_branch_name = "Test"
    folder_path = "Test"
    file_name = "test_file.py"
    file_content = """
    import unittest

    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

    class TestMathOperations(unittest.TestCase):

        def test_add(self):
            self.assertEqual(add(1, 2), 3)
            self.assertEqual(add(-1, 1), 0)
            self.assertEqual(add(-1, -1), -2)

        def test_subtract(self):
            self.assertEqual(subtract(2, 1), 1)
            self.assertEqual(subtract(-1, 1), -2)
            self.assertEqual(subtract(-1, -1), 0)

    if __name__ == '__main__':
        unittest.main()
    """
    create_branch(username, password, project_key, repo_slug, new_branch_name, source_branch_name)
    create_file_in_branch(username, password, project_key, repo_slug, new_branch_name, f"{folder_path}/{file_name}",
                          file_content)
    resp = create_pull_request(
        username=username,
        password=password,
        project_key=project_key,
        repo_slug=repo_slug,
        from_branch=new_branch_name,
        to_branch=source_branch_name,
        title=f"Unit-test {formatted_now}",
        description="Raising a pull request which contains the Unit tests for respective files."
    )
    return resp

send_pr()