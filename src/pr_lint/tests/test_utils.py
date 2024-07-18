from ..utils import collect_emojis_from_labels, extract_owner_from_title, extract_pure_title, extract_reference_number


def test_extract_owner_from_title() -> None:
    title = "This is a PR title @owner"
    assert extract_owner_from_title(title) == "owner"

    title = "This is a PR title"
    assert extract_owner_from_title(title) is None


def test_extract_reference_number() -> None:
    title = "This is a PR title (#123)"
    assert extract_reference_number(title) == "123"

    title = "This is a PR title #123"
    assert extract_reference_number(title) is None


def test_extract_pure_title() -> None:
    title = "🚀 This is a PR title @owner"
    assert extract_pure_title(title) == "This is a PR title"

    title = "This is a PR title @owner"
    assert extract_pure_title(title) == "This is a PR title"

    title = "This is a PR title"
    assert extract_pure_title(title) == title


def test_collect_emojis_from_labels() -> None:
    labels = ["🚀 Type: Feature", "🔥 Impact: Major"]
    assert collect_emojis_from_labels(labels) == ["🔥", "🚀"]

    # different order
    labels = ["🔥 Impact: Major", "🚀 Type: Feature"]
    assert collect_emojis_from_labels(labels) == ["🔥", "🚀"]
