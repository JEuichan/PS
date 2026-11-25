# PS 저장소 규칙

여러 컴퓨터(맥·윈도우·학교 PC)에서 풀고 커밋해도 **충돌이 안 나고, 태그로 찾아볼 수 있게** 하는 규칙이다.

---

## 1. 폴더 구조

```
PS/
├─ README.md              # 태그별 목록 (자동 생성, 손으로 고치지 않음)
├─ CONVENTION.md          # 이 파일
├─ TEMPLATE.md            # 문제 README 복사용
├─ boj/
│  └─ 15668/
│     ├─ README.md        # 문제 정보 + 풀이 과정
│     └─ main.py          # 제출 코드
├─ programmers/
│  └─ 42576/
├─ swea/
├─ codeforces/
├─ leetcode/
└─ etc/
   └─ <출처>-<번호>/       # 예: etc/kakao2024-3
```

- **폴더는 `사이트/문제번호/` 로만 나눈다.** 태그로 폴더를 나누지 않는다.
  - 문제 하나에 태그가 여러 개 붙기 때문에, 태그 폴더에 넣으면 어느 폴더에 넣을지 매번 고민해야 하고 나중에 태그를 바꾸면 폴더를 옮겨야 한다.
  - 태그 분류는 각 문제 README의 `tags`를 읽어서 **루트 `README.md`에 자동으로** 만든다. (5번)
- **경로에는 영어·숫자·`-`만 쓴다.** 한글 문제 제목은 README 안에만 쓴다.
  - 맥과 윈도우가 한글 파일명을 다르게 저장해서, 같은 폴더가 git에서 두 개로 보이거나 충돌이 난다.
- 문제 하나 = 폴더 하나. 다른 컴퓨터에서 같은 문제를 동시에 건드리지 않는 한 충돌이 나지 않는다.

### 폴더 안 파일

| 파일 | 내용 |
|---|---|
| `README.md` | 문제 정보(머리말) + 문제 링크 + 풀이 과정. GitHub에서 폴더를 열면 바로 보인다. |
| `main.<확장자>` | 제출 코드. `main.py`, `main.cpp`, `Main.java`(백준 Java는 클래스명이 `Main`이어야 함) |

- 다시 풀면 새 파일을 만들지 말고 **덮어쓴 뒤 커밋**한다. 이전 코드는 git 기록에 남는다.
- 접근이 완전히 다른 풀이를 같이 남기고 싶을 때만 `main_dp.py`처럼 접근 이름을 붙인다.
- 같은 문제를 다른 언어로 풀면 `main.py`, `main.cpp`를 나란히 둔다.

---

## 2. 문제 README 형식

`TEMPLATE.md`를 복사해서 `README.md`로 쓴다. (아래 티어·태그 값은 형식 예시)

```markdown
---
site: BOJ
id: 15668
title: 방 번호
tier: Silver 3
tags: [bruteforce, bitmask]
link: https://www.acmicpc.net/problem/15668
---

# [BOJ 15668] 방 번호

## 풀이 과정

### 처음 떠올린 방법

### 최종 풀이

### 복잡도

### 틀린 이유 / 배운 점
```

맨 위 `---` 사이 머리말(frontmatter)은 목록 자동 생성에 쓰이므로 **형식을 정확히** 지킨다. GitHub에서는 이 부분이 표로 보인다.

| 필드 | 값 | 예시 |
|---|---|---|
| `site` | 아래 사이트 약어 중 하나 | `BOJ` |
| `id` | 문제 번호 (폴더명과 같게) | `15668` |
| `title` | 문제 이름. `:`가 들어가면 `"..."`로 감싼다 | `방 번호` |
| `tier` | 사이트 표기 그대로 | `Silver 3`, `Lv. 2`, `D3`, `1400` |
| `tags` | `[ ]` 안에 쉼표로. 아래 태그 목록에서 고른다 | `[bruteforce, bitmask]` |
| `link` | 문제 주소 | |

### 사이트 약어

| `site` | 사이트 | 폴더 | `tier` 표기 |
|---|---|---|---|
| `BOJ` | 백준 | `boj/` | `Bronze 5` ~ `Ruby 1`, `Unrated` (solved.ac 기준) |
| `PGS` | 프로그래머스 | `programmers/` | `Lv. 0` ~ `Lv. 5` |
| `SWEA` | SW Expert Academy | `swea/` | `D1` ~ `D8` |
| `CF` | Codeforces | `codeforces/` | 레이팅 숫자 (`1400`) |
| `LC` | LeetCode | `leetcode/` | `Easy` / `Medium` / `Hard` |
| `ETC` | 그 외 | `etc/` | 자유 |

### 태그 목록

철자가 하나라도 다르면 다른 태그로 분류되니까 **이 표에 있는 이름만** 쓴다. 새 태그가 필요하면 이 표와 `scripts/build_index.py`의 `TAG_NAMES`에 같이 추가한다.

| 태그 | 이름 | 태그 | 이름 |
|---|---|---|---|
| `implementation` | 구현 | `simulation` | 시뮬레이션 |
| `math` | 수학 | `number-theory` | 정수론 |
| `combinatorics` | 조합론 | `geometry` | 기하 |
| `bruteforce` | 브루트포스 | `backtracking` | 백트래킹 |
| `recursion` | 재귀 | `divide-and-conquer` | 분할 정복 |
| `greedy` | 그리디 | `sorting` | 정렬 |
| `binary-search` | 이분 탐색 | `parametric-search` | 매개 변수 탐색 |
| `two-pointer` | 투 포인터 | `sliding-window` | 슬라이딩 윈도우 |
| `prefix-sum` | 누적 합 | `bitmask` | 비트마스킹 |
| `dp` | 다이나믹 프로그래밍 | `string` | 문자열 |
| `data-structure` | 자료 구조 | `stack` | 스택 |
| `queue` | 큐 | `deque` | 덱 |
| `heap` | 우선순위 큐 | `hash` | 해시 |
| `graph` | 그래프 이론 | `bfs` | 너비 우선 탐색 |
| `dfs` | 깊이 우선 탐색 | `shortest-path` | 최단 경로 |
| `tree` | 트리 | `union-find` | 분리 집합 |
| `mst` | 최소 스패닝 트리 | `topological-sort` | 위상 정렬 |
| `segment-tree` | 세그먼트 트리 | `trie` | 트라이 |

---

## 3. 커밋 메시지

### 문제 커밋

```
[BOJ 15668] 방 번호
[BOJ 15668] 방 번호 | 재풀이
[PGS 42576] 완주하지 못한 선수
[ETC kakao2024-3] 주사위 고르기
```

- 형식: `[사이트 번호] 문제 이름`
- 같은 문제를 다시 풀거나 풀이를 고치면 뒤에 `| 재풀이`, `| 풀이 보완`을 붙인다.
- **한 문제 = 한 커밋.** 여러 문제를 한 커밋에 섞지 않는다.
- 태그·티어는 README 머리말에 있으니 커밋 메시지에 다시 쓰지 않는다.

### 문제가 아닌 커밋

```
docs: 태그 목록에 trie 추가
chore: .gitignore에 *.exe 추가
```

- `docs:` 규칙 문서·템플릿 수정
- `chore:` 설정, 스크립트, 워크플로 수정

---

## 4. 컴퓨터를 옮겨 다닐 때

```bash
# 시작할 때 항상 먼저
git pull

# 문제 하나 끝날 때마다
git add boj/15668
git commit -m "[BOJ 15668] 방 번호"
git push
```

- 다른 컴퓨터로 넘어가기 전에 **무조건 push**한다. 다 못 풀었으면 `| 미완`을 붙여서 올린다.
- push할 때마다 GitHub Actions가 루트 `README.md`를 다시 만들어서 커밋한다. 그래서 **push 직후에 또 push하면 거절될 수 있는데, 그때는 `git pull` 한 번 하고 다시 push**하면 된다.

### 컴퓨터마다 처음 한 번

```bash
git config --global pull.rebase true              # pull 할 때 merge 커밋 안 생기게
git config --global core.quotepath false          # git status 한글 깨짐 방지
git config --global core.precomposeunicode true   # (맥) 한글 파일명 NFC로 저장
git config --global core.autocrlf input           # (윈도우) 줄바꿈 LF로 커밋
```

줄바꿈은 저장소의 `.gitattributes`가 LF로 맞춰 주므로, 윈도우와 맥에서 번갈아 커밋해도 파일 전체가 바뀐 것처럼 보이지 않는다.

---

## 5. 태그별 목록 자동 생성

- `scripts/build_index.py`가 모든 문제 `README.md`의 머리말을 읽어서, 루트 `README.md`의 `<!-- INDEX:START -->` ~ `<!-- INDEX:END -->` 사이를 다시 쓴다.
- `main`에 push하면 GitHub Actions(`.github/workflows/build-index.yml`)가 자동으로 돌린다.
- 로컬에서 미리 확인하려면 `python3 scripts/build_index.py`를 실행한다. 표에 없는 태그나 빠진 필드가 있으면 경고를 출력한다.
- 루트 `README.md`의 표시 영역 바깥(소개 문구)은 손으로 고쳐도 된다.
