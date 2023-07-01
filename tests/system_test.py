import io
import sys
import unittest
from interpreter import launcher

class SystemTest(unittest.TestCase):

    def test_system(self):

        sys.stdout = io.StringIO()

        expected = ''
        launch = launcher.Launcher('tests/test_file.mnl')
        launch.run_moonlet()
        
        output = sys.stdout.getvalue()
        
        sys.stdout = sys.__stdout__
        self.assertEqual(output, expected, "Launching the System test gave an unexpected output")

if __name__ == '__main__':
    unittest.main()