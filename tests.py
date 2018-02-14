#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Author: aaron@junctionapps.ca
# Project: 3e-timecard

# Copyright 2018 Junction Applications Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
import pytz
from datetime import datetime
from timecard import timecard_attributes

class TestStringMethods(unittest.TestCase):

    def test_tc_attributes(self):
        tz = pytz.timezone('America/Halifax')
        desired = ({'Matter': '136815',
                    'Timekeeper': '3171',
                    'WorkAmt': '500.0',
                    'WIPAmt': '500.0',
                    'WorkHrs': '1.0',
                    'WIPHrs': '1.0',
                    'WorkDate': datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0),
                    'RateCalcList': 'OVR',
                    'Narrative':
                    'Demonstrated time card creation with Python and Zeep'},)
        self.assertEqual(timecard_attributes(), desired)


if __name__ == '__main__':
    unittest.main()
