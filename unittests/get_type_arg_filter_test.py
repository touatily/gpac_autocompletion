import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import autocomplete.gpac_autocomplete as ga


class get_type_arg_filter_test(unittest.TestCase):
    def test_get_type_arg_filter(self):
        list_tests = [
            ("inspect", "deep", ("bool", [])),
            ("inspect", "fmt", ("str", [])),
            ("inspect", "full", ("bool", [])),
            ("inspect", "xml", ("bool", [])),
            ("httpout", "block_size", ("uint", [])),
            ("routein", "repair", ("enum", ["no", "simple", "strict", "full"])),
            ("routein", "repair_urls", ("strl", [])),
            ("routeout", "nozip", ("bool", [])),
            ("inspect", "start", ("dbl", [])),
            ("compositor", "mode2d", ("enum", ['immediate', 'defer', 'debug'])),
        ]

        for test in list_tests:
            res = ga.get_type_arg_filter(test[0], test[1])
            self.assertEqual(res, test[2], "Test failed: _" + test[0] + "." + test[1] + "_")
    