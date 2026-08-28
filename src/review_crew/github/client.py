import requests
import base64
BASE_URL = "https://api.github.com"

class GithubClient:
    def __init__(self, token: str):
        self.token = token

    def get_pr_files(owner: str, repo: str, pr_number: int):
        """Get the files changed in a pull request."""
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_repo_tree(owner: str, repo: str, ref: str):
        """Get the tree of a repository."""
        url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/{ref}"
        response = requests.get(
            url,
            params={"recursive": "1"},
        )
        response.raise_for_status()
        return response.json()

    def get_file(owner: str, repo: str, path: str, ref: str):
        """Get the contents of a certain file in a repository."""
        url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(
            url,
            params={"ref": ref},
        )
        response.raise_for_status()
        return base64.b64decode(response.json()["content"]).decode("utf-8")
