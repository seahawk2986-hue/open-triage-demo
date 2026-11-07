# Receipts for SAMPLE_TRIAGE.md

Target: https://github.com/seahawk2986-hue/apex-ghost-family at commit `758795eb8`. Run on 2026-11-06 with git 2.34.1 and Python 3.10.12 on Linux. Every command below was run exactly as printed, in a checkout of that commit; outputs are copied as they appeared.

## Reproduce

`git clone https://github.com/seahawk2986-hue/apex-ghost-family && cd apex-ghost-family && git checkout 758795eb8`

## Checks

- Files: `git ls-files | wc -l` -> `1121`
- Python files: `git ls-files '*.py' | wc -l` -> `485`
- Top extensions: `git ls-files | sed -E 's/.*\.([A-Za-z0-9]+)$/\1/' | sort | uniq -c | sort -rn | head -5` -> `485 py`, `379 json`, `82 ps1`, `62 jsonl`, `45 md`
- Finding 1: `git grep -lE 'C:\\Users\\' -- '*.py' | wc -l` -> `408`
- Finding 2: `git ls-files | grep -ciE '^(LICENSE|COPYING)'` -> `0`
- Finding 3: `git cat-file -s HEAD:Tools/mcp-publisher.exe` -> `21169152`
- Finding 4: `git ls-files .github/workflows | wc -l` -> `15`; `git grep -lE 'pytest|unittest|selftest' -- .github/workflows | wc -l` -> `1`
- Finding 5: `git ls-files | grep -E '(^|/)(tests?/|test_[^/]*\.py$|[^/]*_test\.py$|[^/]*selftest[^/]*\.py$)'` -> `Scripts/Attic/_checkout_test.py`, `Scripts/Attic/_runner_portable_test.py`, `test_reward.py`
- Finding 6: `wc -c < README.md` -> `1993`; `grep -ciE 'install|quick ?start|usage|getting started|how to run' README.md` -> `0`
- Finding 7: `grep -cvE '^\s*(#|$)' requirements.txt` -> `16`; `grep -cE '==' requirements.txt` -> `7`
- Finding 8: `git ls-files | grep -cE '\.(jsonl|log)$'` -> `69`; `git cat-file -s HEAD:Config/HarvestIndex.jsonl` -> `2750439`; `git cat-file -s HEAD:Config/swebench_pool.json` -> `2834257`
- Finding 9: `git ls-files | grep -ciE '^(SECURITY|CONTRIBUTING|CODE_OF_CONDUCT)'` -> `0`; `git ls-files .github/ISSUE_TEMPLATE | wc -l` -> `0`
- Finding 10: `git ls-tree --name-only HEAD Scripts/ | wc -l` -> `431`

## The patch and its test

Files: [patches/0001-claimcheck-portable-root.diff](patches/0001-claimcheck-portable-root.diff) and [tests/test_claimcheck_portable_root.py](tests/test_claimcheck_portable_root.py).

Run from the repo root, with the test copied into `tests/`:

`python3 -I -B -m unittest discover -s tests -p "test_claimcheck_portable_root.py" -v`

**Before the patch** (the file as committed):

```
test_root_is_this_checkout (test_claimcheck_portable_root.PortableRoot) ... FAIL

======================================================================
FAIL: test_root_is_this_checkout (test_claimcheck_portable_root.PortableRoot)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<checkout>/tests/test_claimcheck_portable_root.py", line 21, in test_root_is_this_checkout
    self.assertTrue(os.path.isdir(mod.ROOT), "ROOT does not exist here: %r" % (mod.ROOT,))
AssertionError: False is not true : ROOT does not exist here: 'C:\\Users\\seaha\\Downloads\\Apex-With-Triggers-Fixed'

----------------------------------------------------------------------
Ran 1 test in 0.023s

FAILED (failures=1)
```

**After** `git apply patches/0001-claimcheck-portable-root.diff`:

```
test_root_is_this_checkout (test_claimcheck_portable_root.PortableRoot) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.022s

OK
```

`git apply --check patches/0001-claimcheck-portable-root.diff` on a clean checkout: `OK`.

## Checksums (SHA-256)

- `patches/0001-claimcheck-portable-root.diff` (522 bytes): `5864b7dc53d7881542e9292dc4920773a05085e85f54035b7ddce4a1a96fe605`
- `tests/test_claimcheck_portable_root.py` (1061 bytes): `3491682783ae96e4b0f7e1fa5f9c6a9e8a4083cf218226deb73a45aef7315898`
