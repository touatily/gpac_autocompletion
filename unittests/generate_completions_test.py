#! /usr/bin/env python3

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../autocomplete')))
import autocomplete.gpac_autocomplete as ga

list_tests = [
    ###### tests about help options
    # Test 1:
    ("gpac -h inspect.d", ['inspect.deep ', 'inspect.dump_data ', 'inspect.dur ', 'inspect.dtype ']),
    # Test 2:
    ("gpac -h inspect.deep", ['inspect.deep ']),
    # Test 3:
    ("gpac -h inspect.f", ['inspect.fmt ', 'inspect.full ', 'inspect.fftmcd ']),
    # Test 4:
    ("gpac -h inspect.full", ['inspect.full ']),
    # Test 5:
    ("gpac -h inspect.xss", []),
    # Test 6:
    ("gpac -h inspect.in", ['inspect.interleave ', 'inspect.info ']),
    # Test 7:
    ("gpac -h httpout.bl", ['httpout.block_size ', 'httpout.blockio ']),
    # Test 8:
    ("gpac -h httpout.block", ['httpout.block_size ', 'httpout.blockio ']),
    # Test 9:
    ("gpac -h jsf", ['jsf ', 'jsf.']),
    # Test 10:
    ("gpac -h routein.repa", ['routein.repair ', 'routein.repair_urls ']), 
    # Test 11:
    ("gpac -h probe", ['probe ', 'probe.']),
    # Test 12:
    ("gpac -h probe.", ['probe.log ']),
    
    ###### tests about filters
    # Test 1:
    ("gpac routein:repa", ['repair', 'repair_urls']),
    # Test 2:
    ("gpac routein:repair", ['repair=', 'repair_urls']),

    ###### tests about modules 
    # Test 1:
    ("gpac -h modul", ['modules ', 'module ']),
    # Test 2:
    ("gpac -h module ", ['gm_alsa.so ', 'gm_x11_out.so ', 'gm_jack.so ', 'gm_caca_out.so ', 'gm_sdl_out.so ', 'gm_pulseaudio.so ', 'gm_validator.so ', 'gm_ft_font.so ', ' ']),
    # Test 3:
    ("gpac -h modules ", ['gm_alsa.so ', 'gm_x11_out.so ', 'gm_jack.so ', 'gm_caca_out.so ', 'gm_sdl_out.so ', 'gm_pulseaudio.so ', 'gm_validator.so ', 'gm_ft_font.so ', ' ']),
    # Test 4:
    ("gpac -h module gm_", ['gm_alsa.so ', 'gm_x11_out.so ', 'gm_jack.so ', 'gm_caca_out.so ', 'gm_sdl_out.so ', 'gm_pulseaudio.so ', 'gm_validator.so ', 'gm_ft_font.so ']),
    # Test 5:
    ("gpac -h module gm_f", ['gm_ft_font.so ']),
    
    ###### tests about protocols
    # Test 1:
    ("gpac -o g", ['gfio://']),
    # Test 2:
    ("gpac -o r", ['rtp://', 'rtsp://', 'rtsph://', 'rtsps://', 'route://']),
    # Test 3:
    ("gpac -o t", ['tcp://', 'tcpu://']),
    # Test 4:
    ("gpac -o u", ['udp://', 'udpu://']),
    # Test 5:
    ("gpac -o h", ['http://', 'https://']),
]

class test_generate_completions(unittest.TestCase):

    # Test with the cursor position at the end of the command line
    def test_completions_at_end(self):
        global list_tests
        for test in list_tests:
            res = ga.generate_completions(test[0], len(test[0]))
            self.assertEqual(res, test[1], "Test failed: _" + test[0] + "_")


    # Test with the cursor position before the last character
    def test_completions_with_random_suffix(self):
        import random
        import string
        global list_tests
        for test in list_tests:
            length = len(test[0])

            # generate a random string
            rlen = random.randint(0, 100)
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=rlen))

            command_line = test[0] + random_string
            res = ga.generate_completions(command_line, length)
            self.assertEqual(res, test[1], "Test failed: _" + command_line + "_")
        


if __name__ == '__main__':
    unittest.main()