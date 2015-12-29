#!/usr/bin/env python3

import mozilla_config
from pathlib import Path
from pprint import pprint

def test_pick_files():
    profile_dir = Path(__file__).parent / 'dummy_firefox_profile'
    pprint( mozilla_config.pick_files(profile_dir) )
    assert False
