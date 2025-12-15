import re
from collections.abc import Iterable

from github.PullRequest import PullRequest

emoji_pattern = (
    "["
    "\U0001f600-\U0001f64f"  # Emoticons
    "\U0001f300-\U0001f5ff"  # Symbols & pictographs
    "\U0001f680-\U0001f6ff"  # Transport & map symbols
    "\U0001f1e0-\U0001f1ff"  # Flags (iOS)
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\u2600-\u26ff"  # Miscellaneous Symbols
    "\u2700-\u27bf"  # Dingbats
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


def extract_reference_number(title: str) -> str | None:
    """
    Extract the reference number from the title.

    Args:
        title: The title of the pull request

    Returns:
        The reference number of the pull request
    """
    pr_number = re.findall(r"\(#(\d+)\)", title.strip())
    if pr_number:
        return pr_number[0]

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
