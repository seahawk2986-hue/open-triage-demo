# Sample triage report: the hub repo itself

> **Automated draft (disclosed).** Drafted by an AI agent working for the founder. Every number below comes from a command you can run yourself; each command and its output is in [RECEIPTS.md](RECEIPTS.md).

- **Target:** [apex-ghost-family](https://github.com/seahawk2986-hue/apex-ghost-family), public, at commit `758795eb8`
- **Why this repo:** it is ours, so you can check every claim. A paid triage is this same format on **your** repo.
- **Reproduce:** `git clone https://github.com/seahawk2986-hue/apex-ghost-family && cd apex-ghost-family && git checkout 758795eb8`
- **Scope of this sample:** repository hygiene and maintainability. Not covered: security review, runtime behavior, performance.

## Summary

1,121 files: 485 Python, 379 JSON, 82 PowerShell, 62 JSONL, 45 Markdown. Ten findings, ordered by impact against effort. Findings 1 to 3 block reuse or trust; 4 to 8 slow every change; 9 and 10 are tidying. A patch and a test for finding 1 ship with this sample: [patches/0001-claimcheck-portable-root.diff](patches/0001-claimcheck-portable-root.diff) and [tests/test_claimcheck_portable_root.py](tests/test_claimcheck_portable_root.py).

## Findings

### 1. High: 408 of 485 Python files hard-code a Windows path (effort: small per file, scriptable)

**Evidence:** `Scripts/ClaimCheck.py` line 27 sets `ROOT` to a fixed `C:\Users\...` folder. 408 of the 485 Python files hard-code a Windows path like it.
**Check:** `git grep -lE 'C:\\Users\\' -- '*.py' | wc -l` -> `408`
**Why it matters:** the code cannot run or be tested on any other machine, Linux CI included, so none of the later findings can be fixed safely until this is.
**Fix:** derive the root from `__file__`. Patch and test are included; the test fails before the patch and passes after (see RECEIPTS).

### 2. High: no license file (effort: tiny)

**Check:** `git ls-files | grep -ciE '^(LICENSE|COPYING)'` -> `0`
**Why it matters:** without a license, others generally have no right to reuse or contribute to the code.
**Fix:** the owner picks a license (MIT and Apache-2.0 are common) and adds `LICENSE`. This is the owner's decision, so no patch is included.

### 3. High: a 21 MB executable is committed (effort: small)

**Check:** `git cat-file -s HEAD:Tools/mcp-publisher.exe` -> `21169152` (bytes)
**Why it matters:** an unexplained binary in a repo is a trust and supply-chain risk, and it bloats every clone. (We did not run it.)
**Fix:** remove it from the repo, document the official download, and record its SHA-256 so users can verify what they fetch.

### 4. Medium: CI does not run tests (effort: small)

**Check:** `git ls-files .github/workflows | wc -l` -> `15`; `git grep -lE 'pytest|unittest|selftest' -- .github/workflows | wc -l` -> `1`
**Why it matters:** there are 15 workflow files but only one mentions a test runner, so changes are not gated by tests.
**Fix:** add a workflow that runs the test suite on every push and pull request, once finding 1 makes the tests portable.

### 5. Medium: very few tests (effort: medium)

**Check:** `git ls-files | grep -E '(^|/)(tests?/|test_[^/]*\.py$|[^/]*_test\.py$|[^/]*selftest[^/]*\.py$)'` -> 3 files: `Scripts/Attic/_checkout_test.py`, `Scripts/Attic/_runner_portable_test.py`, `test_reward.py`
**Why it matters:** 3 test-named files for 485 Python files, and two of them sit in an `Attic` folder.
**Fix:** start with one smoke test per entry-point script. The sample test is the first of these.

### 6. Medium: the README has no install or usage section (effort: tiny)

**Check:** `wc -c < README.md` -> `1993`; `grep -ciE 'install|quick ?start|usage|getting started|how to run' README.md` -> `0`
**Why it matters:** a new reader cannot tell how to run anything.
**Fix:** add a ten-line quick start: prerequisites, install, run, test.

### 7. Medium: dependencies are mostly unpinned (effort: tiny)

**Check:** `grep -cvE '^\s*(#|$)' requirements.txt` -> `16`; `grep -cE '==' requirements.txt` -> `7`
**Why it matters:** 9 of the 16 requirements float to whatever version is newest, so a build that works today can break tomorrow.
**Fix:** pin versions from a known-good environment (`pip freeze`) or add a constraints file.

### 8. Medium: generated data is committed (effort: small)

**Check:** `git ls-files | grep -cE '\.(jsonl|log)$'` -> `69`; `git cat-file -s HEAD:Config/HarvestIndex.jsonl` -> `2750439`; `git cat-file -s HEAD:Config/swebench_pool.json` -> `2834257`
**Why it matters:** 69 runtime `.jsonl` and `.log` files, and a 2.8 MB data file, bloat every clone and make diffs noisy.
**Fix:** stop tracking generated data (`.gitignore`, keep tiny samples) and publish large datasets as release assets.

### 9. Low: no security policy, contributing guide or issue templates (effort: tiny)

**Check:** `git ls-files | grep -ciE '^(SECURITY|CONTRIBUTING|CODE_OF_CONDUCT)'` -> `0`; `git ls-files .github/ISSUE_TEMPLATE | wc -l` -> `0`
**Why it matters:** people have no private way to report a vulnerability and no guidance for contributing.
**Fix:** add `SECURITY.md`, `CONTRIBUTING.md` and bug/triage issue templates.

### 10. Low: 431 entries in one `Scripts/` folder (effort: medium, do last)

**Check:** `git ls-tree --name-only HEAD Scripts/ | wc -l` -> `431`
**Why it matters:** the folder is hard to navigate and review.
**Fix:** group scripts by purpose, but only after finding 1 lands: moving files is risky while paths are hard-coded.

## What a paid triage adds

Your repo and your question; the top fixes as patch diffs; tests that fail before and pass after; run receipts for everything; one revision within 7 days. Order from the [storefront](https://seahawk2986-hue.github.io/apex-ghost-family/).
