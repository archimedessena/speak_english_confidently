import unittest
class TestBasicFunctionality(unittest.TestCase):
    def test_imports(self):
        """Test that all modules can be imported"""
        try:
            from utils.config import Config
            from utils.logger import setup_logger
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")
