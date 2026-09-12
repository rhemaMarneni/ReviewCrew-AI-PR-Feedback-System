import base64
import json
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

BASE_URL = "https://api.github.com"


class GithubClientToolInput(BaseModel):
    """What the agent passes when it calls this tool."""

    action: str = Field(
        ...,
        description="One of: get_pr_metadata, get_pr_files, get_repo_tree, get_file",
    )
    pr_url: str = Field(..., description="GitHub pull request URL")
    path: str = Field(default="", description="File path. Required for get_file.")
    ref: str = Field(default="", description="Optional git ref for get_file.")


class GithubClientTool(BaseTool):
    name: str = "github_client"
    description: str = (
        "Fetch GitHub pull request metadata, changed files, the repository tree, "
        "or a specific file. Always pass the pull request URL."
    )
    args_schema: Type[BaseModel] = GithubClientToolInput
    token: str

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def _parse_pr(self, pr_url: str) -> tuple[str, str, str]:
        print("Parsing PR URL:", pr_url)
        parts = [part for part in pr_url.rstrip("/").split("/") if part]
        # https://github.com/owner/repo/pull/123 -> ['https:', 'github.com', 'owner', 'repo', 'pull', '123']
        try:
            github_index = parts.index("github.com")
            owner, repo, pull, pr_number = parts[github_index + 1 : github_index + 5]
        except (ValueError, IndexError):
            raise ValueError(
                f"Expected a GitHub PR URL like https://github.com/owner/repo/pull/123, got: {pr_url!r}"
            )
        if pull != "pull" or not pr_number.isdigit():
            raise ValueError(
                f"Expected a GitHub PR URL like https://github.com/owner/repo/pull/123, got: {pr_url!r}"
            )
        return owner, repo, pr_number

    def _run(self, action: str, pr_url: str, path: str = "", ref: str = "") -> str:
        """CrewAI calls this when the agent uses the tool."""
        try:
            owner, repo, pr_number = self._parse_pr(pr_url)
            metadata = self.get_pr_metadata(owner, repo, pr_number)

            if action == "get_pr_metadata":
                return json.dumps(metadata, default=str)
            if action == "get_pr_files":
                return json.dumps(self.get_pr_files(owner, repo, pr_number), default=str)
            if action == "get_repo_tree":
                return json.dumps(self.get_repo_tree(owner, repo, metadata["head"]["sha"]), default=str)
            if action == "get_file":
                if not path:
                    return "Error: path is required when action is get_file."
                return self.get_file(owner, repo, path, ref or metadata["head"]["sha"])
            return f"Unknown action: {action}"
        except Exception as exc:
            return f"GitHub API error: {exc}"

    def get_pr_metadata(self, owner: str, repo: str, pr_number: str) -> dict:
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
<<<<<<< Updated upstream:src/review_crew/github/client.py
        self.pr_metadata = response.json()
        print("Fetched PR metadata")
        print(self.pr_metadata)
        return self.pr_metadata
=======
        metadata = response.json()
        print("Fetched PR metadata")
        print(metadata)
        return metadata
>>>>>>> Stashed changes:src/review_crew/services/github_client_service.py

    def get_pr_files(self, owner: str, repo: str, pr_number: str) -> list:
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        files = []
        while url:
            response = requests.get(url, headers=self._headers(), params={"per_page": 100})
            response.raise_for_status()
            files.extend(response.json())
            url = response.links.get("next", {}).get("url")
        print("Fetched files from the PR")
        return files

    def get_repo_tree(self, owner: str, repo: str, ref: str) -> dict:
        url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/{ref}"
        response = requests.get(url, headers=self._headers(), params={"recursive": "1"})
        response.raise_for_status()
        print("Fetched tree from the PR")
        return response.json()

    def get_file(self, owner: str, repo: str, path: str, ref: str) -> str:
        url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self._headers(), params={"ref": ref})
        response.raise_for_status()
        print("Requesting a file...", path)
        return base64.b64decode(response.json()["content"]).decode("utf-8")
