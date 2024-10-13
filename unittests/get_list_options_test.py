import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import autocomplete.gpac_autocomplete as ga

class get_list_options_test(unittest.TestCase):


    def test_get_list_options(self):
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
        
        list_tests_vector = [(test[0], [ord(char) for char in option] if option else []) for test in list_tests for option in test[1]]

        for test in list_tests:
            res = ga.get_list_options(test[0])
            self.assertEqual(res, test[1], "Test failed: _" + test[0] + "_")