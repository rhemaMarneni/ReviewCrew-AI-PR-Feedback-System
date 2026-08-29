import requests
import base64
BASE_URL = "https://api.github.com"

class GithubClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }
        self.owner = None
        self.repo_name = None
        self.pr_number = None
        self.pr_metadata = None

    def get_pr_metadata(self, pr_url: str):
        """Parse a pull request URL and fetch its metadata from GitHub."""
        self.owner, self.repo_name, self.pr_number = pr_url.rstrip("/").split("/")[-4], pr_url.rstrip("/").split("/")[-3], pr_url.rstrip("/").split("/")[-1]

        url = f"{BASE_URL}/repos/{self.owner}/{self.repo_name}/pulls/{self.pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        self.pr_metadata = response.json()
        return self.pr_metadata

    def _require_pr_metadata(self):
        """Raise an error if pull request metadata is not loaded."""
        if self.pr_metadata is None:
            raise ValueError("Pull request metadata must be loaded first.")

    def get_pr_files(self):
        """Get the files changed in a pull request."""
        self._require_pr_metadata()
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo_name}/pulls/{self.pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_repo_tree(self):
        """Get the tree of a repository at PR's head commit."""
        self._require_pr_metadata()
        ref = self.pr_metadata["head"]["sha"]
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo_name}/git/trees/{ref}"
        response = requests.get(url, headers=self.headers, params={"recursive": "1"})
        response.raise_for_status()
        return response.json()

    def get_file(self, path: str, ref: str):
        """Get the contents of a certain file in a repository."""
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo_name}/contents/{path}"
        response = requests.get(
            url,
            headers=self.headers,
            params={"ref": ref},
        )
        response.raise_for_status()
        return base64.b64decode(response.json()["content"]).decode("utf-8")
