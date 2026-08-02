import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover("lib/test", pattern="*_test.py")
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().discover("src/test", pattern="*_test.py")
    unittest.TextTestRunner(verbosity=2).run(suite)