import re
from typing import Iterable

from github.Label import Label
from github.PullRequest import PullRequest

emoji_pattern = re.compile(
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


def format(pr: PullRequest) -> None:
    """
    Format a pull request:

    1. Extract emojis from labels and insert them to the PR title

    Args:
        pr: The pull request to format
    """

    labels: Iterable[Label] = pr.get_labels()
    # remove all emojis from the left of title
    cleaned_title = pr.title.lstrip("".join(emoji_pattern.findall(pr.title))).strip()

    # Sort the labels in the following order
    # any label with "Impact:"
    # any label with "Type:"
    # other labels
    labels = sorted(labels, key=lambda label: ("Impact:" in label.name, "Type:" in label.name), reverse=True)

    emojis = []
    for label in labels:
        if _emjojis := emoji_pattern.findall(label.name):
            for _emjoin in _emjojis:
                if _emjoin not in emojis:
                    emojis.append(_emjoin)

    new_title = f"{''.join(emojis)} {cleaned_title}"
    if new_title != pr.title:
        print(f"Updated PR title: {pr.title} -> {new_title}")
        pr.edit(title=new_title)
