# -*- coding: utf-8 -*-

import unittest
import sqlPuzzle


class SqlPuzzleTest(unittest.TestCase):
    def setUp(self):
        self.sqlPuzzle = sqlPuzzle.SqlPuzzle()

    def tearDown(self):
        self.sqlPuzzle = sqlPuzzle.SqlPuzzle()
    
    def testSelect(self):
        self.sqlPuzzle.select('id', 'name')
        self.sqlPuzzle.from_('user')
        self.sqlPuzzle.where('name', 'John', sqlPuzzle.EQUAL_TO)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user` WHERE `name` = "John"')
    
    def testInsert(self):
        self.sqlPuzzle.insert().into('user')
        self.sqlPuzzle.values({
            'name': 'Harry',
            'sex': 'female', # :)
        })
        self.assertEqual(self.sqlPuzzle.getQuery(), 'INSERT INTO `user` (`name`, `sex`) VALUES ("Harry", "female")')
    
    def testUpdate(self):
        self.sqlPuzzle.update('user')
        self.sqlPuzzle.set(sex='male')
        self.sqlPuzzle.where(name='Harry')
        self.assertEqual(self.sqlPuzzle.getQuery(), 'UPDATE `user` SET `sex` = "male" WHERE `name` = "Harry"')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SqlPuzzleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


