import re
from typing import Iterable

from github.PullRequest import PullRequest

emoji_pattern = (
    "["
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & pictographs
    "\U0001F680-\U0001F6FF"  # Transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\u2600-\u26FF"  # Miscellaneous Symbols
    "\u2700-\u27BF"  # Dingbats
    "]"
)


def extract_owner_from_title(title: str) -> str | None:
    """
    Extract the owner from the title.

    Args:
        title: The title of the pull request

    Returns:
        The owner of the pull request
    """
    pr_owners = re.findall(r"(@[\w-]+)$", title.strip())
    if pr_owners:
        return pr_owners[0][1:]

    return None


def get_owner(pr: PullRequest) -> str | None:
    """
    Get the owner of a pull request.

    Args:
        pr: The pull request

    Returns:
        The owner of the pull request
    """
    if owner := extract_owner_from_title(pr.title):
        return owner

    # if the PR title does not end with a username, check if there is an assignee
    if pr.assignee:
        return pr.assignee.login
    return None


def extract_pure_title(title: str) -> str:
    """
    Extract the title without emojis and the owner.

    Args:
        title: The title to clean

    Returns:
        The title without emojis and the owner
    """
    match_title = re.findall(rf"^{emoji_pattern}*(.*?)(@[\w-]+)?$", title)
    assert match_title, "cannot extract title"
    return match_title[0][0].strip()


def collect_emojis_from_labels(labels: Iterable[str]) -> list[str]:
    """
    Collect emojis from labels.

    Args:
        labels: The labels to collect emojis from

    Returns:
        The emojis from the labels
    """

    # Sort the labels in the following order
    # any label with "Impact:"
    # any label with "Type:"
    # other labels

    labels = sorted(labels, key=lambda label: ("Impact:" in label, "Type:" in label), reverse=True)

    emojis = []
    for label in labels:
        if _emojis := re.findall(emoji_pattern, label):
            for _emoji in _emojis:
                if _emoji not in emojis:
                    emojis.append(_emoji)

    return emojis
