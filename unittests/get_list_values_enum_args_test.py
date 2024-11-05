"""
Unit tests for the `get_list_values_enum_args` function in the `gpac_autocomplete` module.

This module contains a series of tests to verify the correctness of the `get_list_values_enum_args`
function. Each test case consists of a filter string and the expected dictionary of values.
"""
import unittest
import autocomplete.gpac_autocomplete as ga

list_tests = [
    # Test 1:
    ("j2kdec", {}),
    # Test 2:
    ("inspect", {'blk': 'mode', 'bs': 'analyze', 'encode': 'test', 'encx': 'test', 'frame': 'mode',
            'network': 'test', 'netx': 'test', 'no': 'test', 'nobr': 'test', 'nocrc': 'test',
            'noprop': 'test', 'off': 'analyze', 'on': 'analyze', 'pck': 'mode', 'raw': 'mode'}),
    # Test 3:
    ("routeout", {'mcast': 'splitlct', 'meta': 'csum', 'no': 'csum', 'off': 'splitlct',
                  'type': 'splitlct'}),
    # Test 4:
    ("routein", {'full': 'repair', 'no': 'repair', 'simple': 'repair', 'strict': 'repair'}),
    # Test 5:
    ("httpout", {'auto': 'cors', 'default': 'hmode', 'off': 'cors', 'on': 'cors', 'push': 'hmode',
                 'source': 'hmode'}),
    # Test 6:
    ("compositor", {'text': 'aa', 'all': 'aa', 'box': 'bvol', 'aabb': 'bvol', 'default': 'textxt',
                    'never': 'textxt', 'always': 'textxt', 'immediate': 'mode2d', 'defer': 'mode2d',
                    'debug': 'mode2d', 'hybrid': 'ogl', 'walk': 'nav', 'fly': 'nav', 'pan': 'nav',
                    'game': 'nav', 'slide': 'nav', 'exam': 'nav', 'orbit': 'nav', 'vr': 'nav',
                    'alpha': 'bcull', 'only': 'wire', 'solid': 'wire', 'face': 'norms',
                    'vertex': 'norms', 'point': 'depth_gl_type', 'strip': 'depth_gl_type',
                    'hmd': 'stereo', 'ana': 'stereo', 'cols': 'stereo', 'rows': 'stereo',
                    'spv5': 'stereo', 'alio8': 'stereo', 'custom': 'stereo', 'straight': 'camlay',
                    'offaxis': 'camlay', 'linear': 'camlay', 'circular': 'camlay', 'yes': 'drv',
                    'partial': 'tvtd', 'full': 'tvtd', 'base': 'player', 'gui': 'player'}),
]


class GetListValuesEnumArgsTest(unittest.TestCase):

    def test_get_list_values_enum_args(self):
        for test in list_tests:
            res = ga.get_list_values_enum_args(test[0])
            self.assertEqual(res, test[1], "Test failed: filter = " + test[0])
