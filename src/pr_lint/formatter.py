import re

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

    labels = pr.get_labels()
    # remove all emojis from the left of title
    cleaned_title = pr.title.lstrip("".join(emoji_pattern.findall(pr.title))).strip()

    emojis = set()
    for label in labels:
        if _emjojis := emoji_pattern.findall(label.name):
            emojis.update(_emjojis)

    new_title = f"{''.join(emojis)} {cleaned_title}"
    if new_title != pr.title:
        pr.edit(title=new_title)
        print(f"Updated PR title: {pr.title} -> {new_title}")
