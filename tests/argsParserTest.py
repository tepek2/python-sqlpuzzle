# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
from sqlPuzzle.argsParser import parseArgsToListOfTuples as parser


class ArgsParserTest(unittest.TestCase):
    def testDefaultArgs1(self):
        self.assertEqual(parser({}, 1), [(1,)])
    
    def testDefaultArgs2(self):
        self.assertEqual(parser({}, 1, 2), [(1,), (2,)])
    
    def testDefaultList(self):
        self.assertEqual(parser({}, [1,]), [(1,)])
    
    def testDefaultTuple(self):
        self.assertEqual(parser({}, (1,)), [(1,)])
    
    def testDefaultKwdsException(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {}, arg=1)
    
    def testDefaultDictionaryException(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {}, {'key': 1})
        
    def testDefaultTooManyException(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {}, (1, 2))
    
    
    def testMax2Args1(self):
        self.assertEqual(parser({'maxItems': 2}, 1), [(1, None)])
    
    def testMax2Args2(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2), [(1, 2)])
    
    def testMax2Args3(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2, 3), [(1, None), (2, None), (3, None)])
    
    
    def testMin2Max1Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {'minItems': 2})
    
    
    def testMin2Args1Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {'minItems': 2, 'maxItems': 2}, 1)
    
    def testMin2Args2Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {'minItems': 2, 'maxItems': 2}, 1, 2)
    
    def testMin2Tuple(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, (1, 2)), [(1, 2)])
    
    
    def testAllowDictionaryExceptionTooFew(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {'allowDict': True}, 1)
    
    def testAllowDictionaryException(self):
        self.assertRaises(sqlPuzzle.exceptions.ArgsParserException, parser, {'allowDict': True, 'maxItems': 2}, {'key': 1}, 2)
    
    def testAllowDictionary(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, {'key': 1}), [('key', 1)])
    
    def testAllowDictionaryKwds(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, key=1), [('key', 1)])
        
        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ArgsParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

