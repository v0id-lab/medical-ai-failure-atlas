from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


@dataclass(frozen=True)
class MarkdownTarget:
    target: str
    line_number: int


def test_root_readme_local_links_resolve_inside_repo() -> None:
    markdown = README.read_text(encoding="utf-8")
    errors: list[str] = []

    for link in _markdown_targets(markdown):
        path_part, anchor = _split_target(link.target)
        if SCHEME_RE.match(path_part):
            continue

        target_path = README if not path_part else (ROOT / unquote(path_part)).resolve()
        if not _is_inside_repo(target_path):
            errors.append(f"README.md:{link.line_number}: link escapes repository: {link.target}")
            continue
        if not target_path.exists():
            errors.append(f"README.md:{link.line_number}: missing local target: {link.target}")
            continue

        if anchor and target_path.suffix.lower() == ".md":
            anchors = _markdown_anchors(target_path)
            if anchor not in anchors:
                errors.append(
                    f"README.md:{link.line_number}: missing heading #{anchor} in "
                    f"{target_path.relative_to(ROOT)}"
                )

    assert not errors, "\n".join(errors)


def _markdown_targets(markdown: str) -> list[MarkdownTarget]:
    targets: list[MarkdownTarget] = []
    for match in LINK_RE.finditer(markdown):
        raw_target = match.group(1).strip()
        if not raw_target:
            continue
        if raw_target.startswith("<") and raw_target.endswith(">"):
            raw_target = raw_target[1:-1]
        target = raw_target.split()[0]
        line_number = markdown.count("\n", 0, match.start()) + 1
        targets.append(MarkdownTarget(target=target, line_number=line_number))
    return targets


def _split_target(target: str) -> tuple[str, str]:
    path_part, _, raw_anchor = target.partition("#")
    anchor = unquote(raw_anchor).strip().lower()
    return path_part, anchor


def _is_inside_repo(path: Path) -> bool:
    return path == ROOT or ROOT in path.parents


def _markdown_anchors(path: Path) -> set[str]:
    markdown = path.read_text(encoding="utf-8")
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for match in HEADING_RE.finditer(markdown):
        base = _github_heading_slug(match.group(2))
        count = counts.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return anchors


def _github_heading_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.replace("`", "")
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\s-]", "", heading)
    heading = re.sub(r"\s+", "-", heading)
    return heading
