from github.Label import Label
from github.PullRequest import PullRequest

from .utils import get_owner


def lint(pr: PullRequest) -> None:
    """
    Lint a pull request:
    1. checks if the PR title ends with a username (owner)
    2. The username must be a collaborator
    3. checks if there is exactly one Type label
    4. checks if there is exactly one Impact label

    Args:
        pr: The pull request to lint
    """
    owner = get_owner(pr)
    assert owner, "PR title should end with a GitHub username"

    # FIXME: for some reason the has_in_collaborators method is not working
    # pr_owner = pr_owners[0][1:]
    # assert repo.has_in_collaborators(pr_owner), f"{pr_owner} is not a collaborator"

    labels = pr.get_labels()

    type_labels: list[Label] = []
    impact_labels: list[Label] = []

    for label in labels:
        if "Type:" in label.name:
            type_labels.append(label)
        elif "Impact:" in label.name:
            impact_labels.append(label)

    assert len(type_labels) == 1, "There should be exactly one Type label"
    assert len(impact_labels) == 1, "There should be exactly one Impact label"

    # TODO: check if the PR title is in the correct format (e.g. commitlint convention)
