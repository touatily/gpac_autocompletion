import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import autocomplete.gpac_autocomplete as ga

class get_list_compgen_test(unittest.TestCase):


    def test_get_list_compgen(self):
        files = [".test_file1", ".test", ".test_file2", "space file1", ".space file2"]
        dirs = ["test_dir1", ".test_dir2", "space dir1", ".space dir2"]

        os.makedirs("/tmp/test_dir", exist_ok=True)
        for file in files:
            with open("/tmp/test_dir/" + file, "w") as file:
                pass
        for dir in dirs:
            os.makedirs("/tmp/test_dir/" + dir, exist_ok=True)

        list_tests = [
            ("~", ["~/"], ["~/"]),
            ("/home", ["/home/"], ["/home/"]),
            ("/hom", ["/home/"], ["/home/"]),
            ("/tmp", ["/tmp/"], ["/tmp/"]),
            ("/this_does_not_exist", [], []),

            # test with files in /tmp/test_dir
            ("/tmp/test_dir", ["/tmp/test_dir/"], ["/tmp/test_dir/"]),
            ("/tmp/test_dir/.t", ["/tmp/test_dir/.test ", "/tmp/test_dir/.test_dir2/", "/tmp/test_dir/.test_file1 ", "/tmp/test_dir/.test_file2 "], ["/tmp/test_dir/.test_dir2/"]),
            ("/tmp/test_dir/.",['/tmp/test_dir/./', '/tmp/test_dir/.space\\ file2 ', '/tmp/test_dir/.test ', '/tmp/test_dir/.test_dir2/', '/tmp/test_dir/../', '/tmp/test_dir/.test_file1 ',
                                '/tmp/test_dir/.space\\ dir2/', '/tmp/test_dir/.test_file2 '],  ['/tmp/test_dir/./', '/tmp/test_dir/.test_dir2/', '/tmp/test_dir/../', '/tmp/test_dir/.space\\ dir2/']),
            ("/tmp/test_dir/this_does_not_exist", [], []),
            ("/tmp/test_dir/space\\ f", ["/tmp/test_dir/space\\ file1 "], []),
            ("/tmp/test_dir/space\\ ", ["/tmp/test_dir/space\\ dir1/", "/tmp/test_dir/space\\ file1 "], ["/tmp/test_dir/space\\ dir1/"]),
            ("/tmp/test_dir/.space\\ d", ["/tmp/test_dir/.space\\ dir2/"], ["/tmp/test_dir/.space\\ dir2/"]),
        ]

        for test in list_tests:
            res = ga.get_list_compgen(test[0], only_dirs=False)
            self.assertEqual(res, test[1], "Test failed (files + dirs): _" + test[0] + "_")


        
        for test in list_tests:
            res = ga.get_list_compgen(test[0], only_dirs=True)
            self.assertEqual(res, test[2], "Test failed (dirs): _" + test[0] + "_")


    
        # delete the files in /tmp/test_dir and dir itself
        for file in files:
            os.remove("/tmp/test_dir/" + file)
        for dir in dirs:
            os.rmdir("/tmp/test_dir/" + dir)
        os.rmdir("/tmp/test_dir")

