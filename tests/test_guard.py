import unittest
import os, sys

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
print(APP_PATH)
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from FileManager.Operations import Guard

class TestFileManager(unittest.TestCase):
    def test_Guard_Check_Permission(self):
        # Initialize Guard with test data
        guard = Guard()
        guard.security_info = {
            "permit": {
                "R": [
                    os.path.abspath("/a/b/c"),
                    os.path.abspath("/a/b/d"),
                    os.path.abspath("/a/b/e/f")
                ]
            },
            "exclude": {
                "R": [
                    os.path.abspath("/a/b/e"),
                    os.path.abspath("/a/b/d/g")
                ]
            }
        }

        # Test cases
        self.assertFalse(guard.Check("/a/b", "R"))  # No permit match
        self.assertTrue(guard.Check("/a/b/c", "R"))  # Permit match
        self.assertTrue(guard.Check("/a/b/c/h/i", "R"))  # Sub-path of permit
        self.assertTrue(guard.Check("/a/b/d", "R"))  # Permit match
        self.assertTrue(guard.Check("/a/b/d/j", "R"))  # Sub-path of permit
        self.assertFalse(guard.Check("/a/b/d/g", "R"))  # Excluded path
        self.assertFalse(guard.Check("/a/b/d/g/k", "R"))  # Sub-path of excluded
        self.assertFalse(guard.Check("/a/b/e", "R"))  # Excluded path
        self.assertFalse(guard.Check("/a/b/e/l", "R"))  # Sub-path of excluded
        self.assertTrue(guard.Check("/a/b/e/f", "R"))  # Permit overrides exclusion
        self.assertTrue(guard.Check("/a/b/e/f/m", "R"))  # Sub-path of permit

if __name__ == "__main__":
    unittest.main()