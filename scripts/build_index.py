"""문제 README 머리말을 읽어 루트 README.md에 태그별 목록을 만든다.

사용법: python3 scripts/build_index.py
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "README.md"
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"

SITE_NAMES = {
    "BOJ": "백준",
    "PGS": "프로그래머스",
    "SWEA": "SWEA",
    "CF": "Codeforces",
    "LC": "LeetCode",
    "ETC": "기타",
}

# CONVENTION.md의 태그 목록과 같게 유지한다. 순서 = README에 나오는 순서.
TAG_NAMES = {
    "implementation": "구현",
    "simulation": "시뮬레이션",
    "math": "수학",
    "number-theory": "정수론",
    "combinatorics": "조합론",
    "geometry": "기하",
    "bruteforce": "브루트포스",
    "backtracking": "백트래킹",
    "recursion": "재귀",
    "divide-and-conquer": "분할 정복",
    "greedy": "그리디",
    "sorting": "정렬",
    "binary-search": "이분 탐색",
    "parametric-search": "매개 변수 탐색",
    "two-pointer": "투 포인터",
    "sliding-window": "슬라이딩 윈도우",
    "prefix-sum": "누적 합",
    "bitmask": "비트마스킹",
    "dp": "다이나믹 프로그래밍",
    "string": "문자열",
    "data-structure": "자료 구조",
    "stack": "스택",
    "queue": "큐",
    "deque": "덱",
    "heap": "우선순위 큐",
    "hash": "해시",
    "graph": "그래프 이론",
    "bfs": "너비 우선 탐색",
    "dfs": "깊이 우선 탐색",
    "shortest-path": "최단 경로",
    "tree": "트리",
    "union-find": "분리 집합",
    "mst": "최소 스패닝 트리",
    "topological-sort": "위상 정렬",
    "segment-tree": "세그먼트 트리",
    "trie": "트라이",
}

LANGS = {
    ".py": "Python",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".java": "Java",
    ".kt": "Kotlin",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".swift": "Swift",
}

REQUIRED = ("site", "id", "title", "tier", "tags", "link")
SKIP_DIRS = {".git", ".github", "scripts"}


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if key == "tags":
            value = [t.strip().strip("'\"") for t in value.strip("[]").split(",") if t.strip()]
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        meta[key] = value
    return None  # 닫는 --- 없음


def cell(text):
    return str(text).replace("|", "\\|")


def collect(warnings):
    problems = []
    for readme in sorted(ROOT.rglob("README.md")):
        rel = readme.relative_to(ROOT)
        if readme == INDEX_FILE or rel.parts[0] in SKIP_DIRS:
            continue
        meta = parse_frontmatter(readme.read_text(encoding="utf-8"))
        if meta is None:
            warnings.append(f"{rel}: 머리말(---)이 없거나 닫히지 않음")
            continue
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            warnings.append(f"{rel}: 빠진 필드 {', '.join(missing)}")
        if meta.get("site") and meta["site"] not in SITE_NAMES:
            warnings.append(f"{rel}: 알 수 없는 site '{meta['site']}'")
        for tag in meta.get("tags") or []:
            if tag not in TAG_NAMES:
                warnings.append(f"{rel}: 목록에 없는 태그 '{tag}'")
        for key in ("title", "tier"):
            if key in meta:
                meta[key] = unicodedata.normalize("NFC", meta[key])
        folder = readme.parent
        langs = sorted({LANGS[p.suffix] for p in folder.iterdir() if p.suffix in LANGS})
        meta["langs"] = langs
        meta["path"] = folder.relative_to(ROOT).as_posix()
        problems.append(meta)
    return problems


def sort_key(p):
    site_order = list(SITE_NAMES).index(p.get("site")) if p.get("site") in SITE_NAMES else len(SITE_NAMES)
    pid = str(p.get("id", ""))
    return (site_order, int(pid) if pid.isdigit() else float("inf"), pid)


def row(p):
    site = SITE_NAMES.get(p.get("site"), p.get("site", ""))
    title = cell(p.get("title", ""))
    link = p.get("link")
    title_cell = f"[{title}]({link})" if link else title
    return (
        f"| {site} | {cell(p.get('id', ''))} | {title_cell} | {cell(p.get('tier', ''))} "
        f"| {', '.join(p['langs'])} | [풀이]({p['path']}) |"
    )


def render(problems):
    out = [f"총 **{len(problems)}** 문제", ""]
    if not problems:
        return "\n".join(out)

    counts = {}
    for p in problems:
        counts[p.get("site")] = counts.get(p.get("site"), 0) + 1
    out += ["| 사이트 | 문제 수 |", "|---|---|"]
    for site in list(SITE_NAMES) + sorted(k for k in counts if k not in SITE_NAMES):
        if site in counts:
            out.append(f"| {SITE_NAMES.get(site, site)} | {counts[site]} |")
    out.append("")

    by_tag = {}
    for p in problems:
        for tag in p.get("tags") or ["untagged"]:
            by_tag.setdefault(tag, []).append(p)
    known = [t for t in TAG_NAMES if t in by_tag]
    unknown = sorted(t for t in by_tag if t not in TAG_NAMES)

    out += ["## 태그별", ""]
    out.append(" · ".join(f"[{TAG_NAMES.get(t, t)} ({len(by_tag[t])})](#tag-{t})" for t in known + unknown))
    out.append("")
    for tag in known + unknown:
        items = sorted(by_tag[tag], key=sort_key)
        out += [
            f'<a id="tag-{tag}"></a>',
            f"### {TAG_NAMES.get(tag, tag)} `{tag}` ({len(items)})",
            "",
            "| 사이트 | 번호 | 문제 | 난이도 | 언어 | 풀이 |",
            "|---|---|---|---|---|---|",
        ]
        out += [row(p) for p in items]
        out.append("")
    return "\n".join(out).rstrip()


def main():
    warnings = []
    problems = collect(warnings)
    text = INDEX_FILE.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"README.md에 {START} / {END} 표시가 없음")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{START}\n{render(problems)}\n{END}{tail}"
    if new != text:
        INDEX_FILE.write_text(new, encoding="utf-8")
        print(f"README.md 갱신 ({len(problems)}문제)")
    else:
        print(f"변경 없음 ({len(problems)}문제)")
    for w in warnings:
        print(f"경고: {w}")


if __name__ == "__main__":
    main()
