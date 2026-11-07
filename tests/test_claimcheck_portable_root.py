"""Sample test (open-triage-demo): ClaimCheck must not depend on one machine's path.

Copy this file into tests/ of a checkout of apex-ghost-family and run:
    python3 -m unittest discover -s tests -p "test_claimcheck_portable_root.py" -v
It fails on the unpatched file (the hard-coded Windows root does not exist on your
machine) and passes once ROOT is derived from __file__.
"""
import importlib.util
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PortableRoot(unittest.TestCase):
    def test_root_is_this_checkout(self):
        path = os.path.join(REPO, "Scripts", "ClaimCheck.py")
        spec = importlib.util.spec_from_file_location("ClaimCheck", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # importing has no side effects
        self.assertTrue(os.path.isdir(mod.ROOT), "ROOT does not exist here: %r" % (mod.ROOT,))
        self.assertEqual(os.path.realpath(mod.ROOT), os.path.realpath(REPO))


if __name__ == "__main__":
    unittest.main()
