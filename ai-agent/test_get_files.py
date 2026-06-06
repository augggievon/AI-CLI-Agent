import os 
import unittest

from functions.write_to_files import write_to_files

class TestWriteFile(unittest.TestCase):
    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertIn("Successfully wrote to", result)

    def test_write_file_nested(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertIn("Successfully wrote to", result)

    def test_write_file_outside_working_directory(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
