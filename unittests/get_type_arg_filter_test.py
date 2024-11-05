"""
Unit tests for the `get_type_arg_filter` function in the `autocomplete.gpac_autocomplete` module.
This test suite includes various test cases to verify the correct functionality of the
`get_type_arg_filter` function.
Each test case checks if the function returns the expected type and argument filter for given
inputs.
"""
import unittest
import autocomplete.gpac_autocomplete as ga


class GetTypeArgFilterTest(unittest.TestCase):
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
    