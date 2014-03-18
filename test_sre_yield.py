#!/usr/bin/env python2
#
# Copyright 2011-2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import sre_yield

class YieldTest(unittest.TestCase):
    """Test that regular expressions give the right lists."""

    def testSimpleCases(self):
        self.assertSequenceEqual(sre_yield.Values('1(234?|49?)'),
                                 ['123', '1234', '14', '149'])
        self.assertSequenceEqual(sre_yield.Values('asd|def'),
                                 ['asd', 'def'])
        self.assertSequenceEqual(sre_yield.Values('asd|def\\+|a\\.b\\.c'),
                                 ['asd', 'def+', 'a.b.c'])

    def testOtherCases(self):
        self.assertSequenceEqual(sre_yield.Values('[aeiou]'), list('aeiou'))
        self.assertEquals(len(sre_yield.Values('1.3')), 256)
        v = sre_yield.Values('[^-]3[._]1415')
        print list(v)
        self.assertEquals(len(v), 510)
        self.assertEquals(len(sre_yield.Values('(.|5[6-9]|[6-9][0-9])[a-z].?')),
                          300 * 26 * 257)
        self.assertEquals(len(sre_yield.Values('..', charset='0123456789')),
                          100)
        self.assertEquals(len(sre_yield.Values('0*')), 65536)
        # For really big lists, we can't use the len() function any more
        self.assertEquals(sre_yield.Values('0*').__len__(), 65536)
        self.assertEquals(sre_yield.Values('[01]*').__len__(), 2 ** 65536 - 1)

    def testAlternationWithEmptyElement(self):
        self.assertSequenceEqual(sre_yield.Values('a(b|c|)'),
                                 ['ab', 'ac', 'a'])
        self.assertSequenceEqual(sre_yield.Values('a(|b|c)'),
                                 ['a', 'ab', 'ac'])
        self.assertSequenceEqual(sre_yield.Values('a[bc]?'),
                                 ['a', 'ab', 'ac'])
        self.assertSequenceEqual(sre_yield.Values('a[bc]??'),
                                 ['a', 'ab', 'ac'])

    def testSlices(self):
        parsed = sre_yield.Values('[abcdef]')
        self.assertSequenceEqual(parsed[::2], list('ace'))
        self.assertSequenceEqual(parsed[1::2], list('bdf'))
        self.assertSequenceEqual(parsed[1:-1], list('bcde'))
        self.assertSequenceEqual(parsed[1:-2], list('bcd'))
        self.assertSequenceEqual(parsed[1:99], list('bcdef'))
        self.assertSequenceEqual(parsed[1:1], [])

        self.assertEquals(parsed[1], 'b')
        self.assertEquals(parsed[-2], 'e')
        self.assertEquals(parsed[-1], 'f')

    def testGetItemNegative(self):
        parsed = sre_yield.Values('x|[a-z]{1,5}')
        self.assertEquals(parsed[0], 'x')
        self.assertEquals(parsed[1], 'a')
        self.assertEquals(parsed[23], 'w')
        self.assertEquals(parsed[24], 'x')
        self.assertEquals(parsed[25], 'y')
        self.assertEquals(parsed[26], 'z')
        self.assertEquals(parsed[27], 'aa')
        self.assertEquals(parsed[28], 'ab')
        self.assertEquals(parsed[-2], 'zzzzy')
        self.assertEquals(parsed[-1], 'zzzzz')

        # last, and first
        parsed.get_item(len(parsed)-1)
        parsed.get_item(-len(parsed))

        # precisely 1 out of bounds
        self.assertRaises(IndexError, parsed.get_item, len(parsed))
        self.assertRaises(IndexError, parsed.get_item, -len(parsed)-1)

    def testContains(self):
        parsed = sre_yield.Values('[01]+')
        self.assertTrue('0101' in parsed)
        self.assertFalse('0201' in parsed)

    def testNaturalOrder(self):
        parsed = sre_yield.Values('[0-9]{2}')
        self.assertEquals(parsed[0], '00')
        self.assertEquals(parsed[1], '01')
        self.assertEquals(parsed[98], '98')
        self.assertEquals(parsed[99], '99')


if __name__ == '__main__':
    unittest.main()