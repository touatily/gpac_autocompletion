import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import autocomplete.gpac_autocomplete as ga

class get_list_args_test(unittest.TestCase):


    def test_get_list_args(self):
        list_tests = [
            ("j2kdec", []),
            ("aout", ["drv", "bnum", "bdur", "threaded", "dur", "clock", "speed", "start", "vol", "pan", "buffer", "mbuffer", "rbuffer", "adelay", "buffer_done", "rebuffer", "media_offset"]),
            ("vout", ['drv', 'vsync', 'drop', 'disp', 'start', 'dur', 'speed', 'hold', 'linear', 'back', 'wsize', 'wpos', 'vdelay', 'hide', 'fullscreen', 'buffer', 'mbuffer', 'rbuffer', 'dumpframes', 'out', 'step', 'async', 'olwnd', 'olsize', 'oldata', 'owsize', 'buffer_done', 'rebuffer', 'vjs', 'media_offset', 'wid', 'vflip', 'vrot', 'oltxt']),
            ("inspect", ['log', 'mode', 'interleave', 'deep', 'props', 'dump_data', 'fmt', 'hdr', 'allp', 'info', 'full', 'pcr', 'speed', 'start', 'dur', 'analyze', 'xml', 'crc', 'fftmcd', 'dtype', 'buffer', 'mbuffer', 'rbuffer', 'stats', 'test']),
            ("httpout", ['dst', 'port', 'ifce', 'rdirs', 'wdir', 'cert', 'pkey', 'block_size', 'user_agent', 'close', 'maxc', 'maxp', 'cache_control', 'hold', 'hmode', 'timeout', 'ext', 'mime', 'quit', 'post', 'dlist', 'sutc', 'cors', 'reqlog', 'ice', 'max_client_errors', 'max_cache_segs', 'reopen', 'max_async_buf', 'blockio', 'ka', 'hdrs', 'js', 'zmax', 'cte', 'maxs', 'norange']),
            ("routeout", ['dst', 'ext', 'mime', 'ifce', 'carousel', 'first_port', 'ip', 'ttl', 'bsid', 'mtu', 'splitlct', 'korean', 'llmode', 'brinc', 'noreg', 'runfor', 'nozip', 'furl', 'flute', 'csum', 'recv_obj_timeout', 'errsim', 'use_inband', 'ssm']),
            ("routein", ['src', 'ifce', 'gcache', 'tunein', 'buffer', 'timeout', 'nbcached', 'kc', 'skipr', 'stsi', 'stats', 'tsidbg', 'max_segs', 'odir', 'reorder', 'cloop', 'rtimeout', 'fullseg', 'repair', 'repair_urls', 'max_sess', 'llmode', 'dynsel']),
            ("cryptout", ['dst', 'fullfile']),
        ]

        for test in list_tests:
            res = ga.get_list_args(test[0])
            res = list(res.keys())
            self.assertEqual(res, test[1], "Test failed: _" + test[0] + "_")

    
    def test_get_list_args_with_types(self):
        list_tests_with_types = [
            ("j2kdec", {}),
            ("bssplit", {'ltid': 'strl', 'sig_ltid': 'bool', 'svcqid': 'bool'}),
            ("uncvdec", {'force_pf': 'bool', 'no_tile': 'bool'}),
            ("avidmx", {'fps': 'frac', 'importer': 'bool', 'noreframe': 'bool'}),
            ("nhmlr", {'index': 'dbl', 'reframe': 'bool'}),
        ]

        for test in list_tests_with_types:
            res = ga.get_list_args(test[0])
            self.assertEqual(res, test[1], "Test failed: _" + test[0] + "_")