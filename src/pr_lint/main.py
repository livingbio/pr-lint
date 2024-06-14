import os
import re

import typer
from github import Github, Label

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & pictographs
    "\U0001F680-\U0001F6FF"  # Transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "]+"
)

app = typer.Typer()


def extract_emoji(string: str) -> set[str]:
    """
    Extracts emojis from a string

    Args:
        string: The string to extract emojis from

    Returns:
        A set of emojis
    """
    return set(emoji_pattern.findall(string))


def clean_title(input_string: str) -> str:
    # remove starting and ending emojis
    input_string = input_string.strip().rstrip("".join(extract_emoji(input_string)))
    input_string = input_string.strip().lstrip("".join(extract_emoji(input_string)))
    input_string = input_string.strip()

    # TODO:
    # rewrite title's type and scope?
    # remove starting type and scope [\w]+:
    # input_string = re.sub(r"^[\w\-\(\)\.]+:", "", input_string).strip()
    return input_string


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

    labels = pr.get_labels()

    type_labels: list[Label.Label] = []
    other_labels: list[Label.Label] = []

    for label in labels:
        if "Type:" in label.name:
            type_labels.append(label)
        else:
            other_labels.append(label)

    assert len(type_labels) == 1, "There should be exactly one Type label"

    # format new title as [Type Emoji][Title][Other Emojis]

    type_emoji = "".join(extract_emoji(type_labels[0].name))
    other_emojis = set()
    for label in other_labels:
        other_emojis.update(extract_emoji(label.name))
    other_emojis_result = "".join(other_emojis)

    new_title = clean_title(pr.title)
    new_title = f"{type_emoji}{new_title}{other_emojis_result}"

    if new_title != pr.title:
        pr.edit(title=new_title)
        print(f"Title changed from {pr.title} to {new_title}")
    else:
        print("Title is already correctly formatted")


if __name__ == "__main__":
    app()
