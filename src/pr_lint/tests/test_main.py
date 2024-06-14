import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from ..main import clean_title, extract_emoji


@pytest.mark.parametrize(
    "title",
    [
        ("🐛fix: correct typo🐛"),
        ("🚀feature(add-new): add a new feature🚀"),
        ("bug: fix issue 🐞"),
        ("no type"),
        ("not an emoji prefix: but contains 🚀 emoji"),
        ("🍎update(v2.0): version update🍎"),
        ("fix: correct typo"),
        ("feature(add-new): add a new feature"),
        ("修复：更正登录方法中的错字"),
        ("🐛修复: correct typo🐛"),
    ],
)
def test_clean_title(title: str, snapshot: SnapshotAssertion) -> None:
    assert snapshot(extension_class=JSONSnapshotExtension) == clean_title(title)


@pytest.mark.parametrize(
    "title, expected",
    [
        ("🐛fix: correct typo🐛", {"🐛"}),
        ("🚀feature(add-new): add a new feature🚀", {"🚀"}),
        ("✨Type: Feature", {"✨"}),
        ("bug: fix issue 🐞", {"🐞"}),
        ("no type", set()),
        ("not an emoji prefix: but contains 🚀 emoji", {"🚀"}),
        ("🍎update(v2.0): version update🚀", {"🚀", "🍎"}),
        ("fix: correct typo", set()),
        ("feature(add-new): add a new feature", set()),
        ("修复：更正登录方法中的错字", set()),
        ("🐛修复: correct typo🐛", {"🐛"}),
    ],
)
def test_extract_emoji(title: str, expected: str) -> None:
    assert extract_emoji(title) == expected
