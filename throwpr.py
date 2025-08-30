import requests
from datetime import datetime
import json
from langchain_core.tools import tool
from repofetch import implementation

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

def get_github_headers(token):
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

def create_branch_github(token, owner, repo, new_branch_name, source_branch_name):
    """Create a new branch on GitHub"""
    # Get the SHA of the source branch
    source_url = f"https://api.github.com/repos/{owner}/{repo}/branches/{source_branch_name}"
    source_response = requests.get(source_url, headers=get_github_headers(token))
    if source_response.status_code != 200:
        print(f"Failed to get source branch: {source_response.status_code}")
        return False
    
    source_sha = source_response.json()['commit']['sha']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/{new_branch_name}",
        "sha": source_sha
    }
    
    response = requests.post(url, json=payload, headers=get_github_headers(token))
    if response.status_code == 201:
        print("Branch created successfully on GitHub.")
        return True
    else:
        print(f"Failed to create branch: {response.status_code}")
        print(response.json())
        return False

def create_file_in_github(token, owner, repo, branch_name, file_path, file_content, commit_message):
    """Create a file in GitHub repository"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
    payload = {
        "message": commit_message,
        "content": file_content.encode('utf-8').decode('latin-1'),
        "branch": branch_name
    }
    
    response = requests.put(url, json=payload, headers=get_github_headers(token))
    if response.status_code in [200, 201]:
        print(f"File {file_path} created successfully in branch {branch_name}.")
        return True
    else:
        print(f"Failed to create file {file_path}: {response.status_code}")
        print(response.json())
        return False

def create_pull_request_github(token, owner, repo, from_branch, to_branch, title, description):
    """Create a pull request on GitHub"""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    payload = {
        "title": title,
        "body": description,
        "head": from_branch,
        "base": to_branch
    }
    
    response = requests.post(url, json=payload, headers=get_github_headers(token))
    if response.status_code == 201:
        print("Pull request created successfully on GitHub.")
        return response.json()
    else:
        print(f"Failed to create pull request: {response.status_code}")
        print(response.json())
        return None

@tool
def send_pr():
    """
    GitHub implementation for creating test files and raising pull requests
    """
    with open('config.json', 'r') as file:
        config = json.load(file)

    token = config['github']['token']
    username = config['github']['username']
    repo_owner = config['github']['repo_owner']
    repo_name = config['github']['repo_name']

    source_branch_name = "main"  # Default to main branch
    new_branch_name = "test-branch-" + formatted_now.replace(" ", "-").replace(":", "-")
    folder_path = "tests"
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

    # Create branch
    branch_created = create_branch_github(token, repo_owner, repo_name, new_branch_name, source_branch_name)
    if not branch_created:
        print("Branch creation failed. Exiting...")
        return

    # Create test file
    file_path = f"{folder_path}/{file_name}"
    commit_message = f"Add test file {file_name}"
    
    create_file_in_github(token, repo_owner, repo_name, new_branch_name, file_path, file_content, commit_message)

    # Create pull request
    resp = create_pull_request_github(
        token=token,
        owner=repo_owner,
        repo=repo_name,
        from_branch=new_branch_name,
        to_branch=source_branch_name,
        title=f"Add Test File - {formatted_now}",
        description="This PR adds a test file for demonstration purposes."
    )

    return resp

# Test the function
if __name__ == "__main__":
    send_pr()