import os

import typer
from github import Github

from .formatter import format
from .linter import lint

app = typer.Typer()


@app.command()
def main() -> None:
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    assert token, "Missing GITHUB_TOKEN environment variable"
    assert repo_name, "Missing GITHUB_REPOSITORY environment variable"
    assert pr_number, "Missing PR_NUMBER environment variable"

    # Authenticate to GitHub
    g = Github(token)

    # Get the repository
    repo = g.get_repo(repo_name)

    # Get the pull request
    pr = repo.get_pull(int(pr_number))

    lint(pr)
    format(pr)


if __name__ == "__main__":
    app()
