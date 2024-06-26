from typing import Iterable

from github.Label import Label
from github.PullRequest import PullRequest

from .utils import collect_emojis_from_labels, extract_pure_title, get_owner


def format(pr: PullRequest) -> None:
    """
    Format a pull request:

    1. Extract emojis from labels and insert them to the PR title

    Args:
        pr: The pull request to format
    """

    labels: Iterable[Label] = pr.get_labels()
    # remove all emojis from the left of title
    cleaned_title = extract_pure_title(pr.title)

    emojis = collect_emojis_from_labels(label.name for label in labels)

    owner = get_owner(pr)

    new_title = f"{''.join(emojis)} {cleaned_title} @{owner}"
    if new_title != pr.title:
        print(f"Updated PR title: {pr.title} -> {new_title}")
        pr.edit(title=new_title)
