import unittest

from functions.run_python_file import run_python_file
# If your function is named execute_python_file instead, use:
# from functions.run_python_file import execute_python_file as run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_usage_instructions(self):
        # run_python_file("calculator", "main.py")
        result = run_python_file("calculator", "main.py")
        print(result)
        # Should succeed and mention usage or help; keep assertion loose
        self.assertNotIn("Error:", result)

    def test_calculator_expression(self):
        # run_python_file("calculator", "main.py", ["3 + 5"])
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)
        # Should run the calculator; just ensure no obvious error
        self.assertNotIn("Error:", result)

    def test_run_calculator_tests(self):
        # run_python_file("calculator", "tests.py")
        result = run_python_file("calculator", "tests.py")
        print(result)
        # The tests inside calculator should run successfully
        self.assertNotIn("Error:", result)
        self.assertNotIn("Process exited with code", result)

    def test_outside_working_directory(self):
        # run_python_file("calculator", "../main.py")
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertTrue(result.startswith('Error: Cannot execute'))

    def test_nonexistent_file(self):
        # run_python_file("calculator", "nonexistent.py")
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertIn('does not exist or is not a regular file', result)

    def test_not_python_file(self):
        # run_python_file("calculator", "lorem.txt")
        result = run_python_file("calculator", "lorem.txt")
        print(result)
        self.assertIn('is not a Python file', result)


if __name__ == "__main__":
    unittest.main()
