# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.argsParser
import sqlPuzzle.exceptions
import sqlPuzzle.sqlValue
import sqlPuzzle.relations


class Condition:
    __defaultRelations = {
        str: sqlPuzzle.relations.EQ,
        unicode: sqlPuzzle.relations.EQ,
        int: sqlPuzzle.relations.EQ,
        long: sqlPuzzle.relations.EQ,
        float: sqlPuzzle.relations.EQ,
        bool: sqlPuzzle.relations.EQ,
        list: sqlPuzzle.relations.IN,
        tuple: sqlPuzzle.relations.IN,
    }
    
    def __init__(self):
        """
        Initialization of Condition.
        """
        self._column = None
        self._value = None
        self._relation = None
    
    def __str__(self):
        """
        Print condition (part of WHERE).
        """
        return '`%s` %s %s' % (
            self._column,
            sqlPuzzle.relations.RELATIONS[self._relation],
            sqlPuzzle.sqlValue.sqlValue(self._value),
        )
    
    def __eq__(self, other):
        return (
            self._column == other._column and
            self._value == other._value and
            self._relation == other._relation
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __isRelationAllowed(self, relation):
        if isinstance(self._value, (str, unicode)):
            return relation in (
                sqlPuzzle.relations.EQ,
                sqlPuzzle.relations.NE,
                sqlPuzzle.relations.GT,
                sqlPuzzle.relations.GE,
                sqlPuzzle.relations.LT,
                sqlPuzzle.relations.LE,
                sqlPuzzle.relations.LIKE,
            )
        # bool is instance of int too, therefor bool must be before int
        elif isinstance(self._value, (bool,)):
            return relation in (
                sqlPuzzle.relations.EQ,
                sqlPuzzle.relations.NE,
            )
        elif isinstance(self._value, (int, long, float)):
            return relation in (
                sqlPuzzle.relations.EQ,
                sqlPuzzle.relations.NE,
                sqlPuzzle.relations.GT,
                sqlPuzzle.relations.GE,
                sqlPuzzle.relations.LT,
                sqlPuzzle.relations.LE,
            )
        elif isinstance(self._value, (list, tuple)):
            return relation in (
                sqlPuzzle.relations.IN,
                sqlPuzzle.relations.NOT_IN,
            )
        return False
    
    def set(self, column, value, relation=None):
        """
        Set column, value and relation.
        """
        self.setColumn(column)
        self.setValue(value)
        self.setRelation(relation or self.__defaultRelations[type(value)])
    
    def setColumn(self, column):
        """
        Set column.
        """
        self._column = column
    
    def setValue(self, value):
        """
        Set value.
        """
        self._value = value
    
    def setRelation(self, relation):
        """
        Set relation.
        """
        if not self.__isRelationAllowed(relation):
            raise sqlPuzzle.exceptions.InvalidArgumentException(
                'Relation "%s" is not allowed for data type "%s".' % (
                    sqlPuzzle.relations.RELATIONS.get(relation, 'undefined'),
                    type(self._value)
                )
            )
        
        self._relation = relation


class Conditions:
    _conditionObject = Condition
    
    def __init__(self):
        """
        Initialization of Conditions.
        """
        self._conditions = []
    
    def __str__(self):
        """
        Print limit (part of query).
        """
        if self.isSet():
            return "WHERE %s" % " AND ".join(str(condition) for condition in self._conditions)
        return ""
    
    def __eq__(self, other):
        return all(bool(sc == oc) for sc, oc in zip(self._conditions, other._conditions))
    
    def __contains__(self, item):
        for condition in self._conditions:
            if item == condition:
                return True
        return False
    
    def isSet(self):
        """
        Is where set?
        """
        return self._conditions != []
    
    def where(self, *args, **kwds):
        """
        Set condition(s).
        """
        for column, value, relation in sqlPuzzle.argsParser.parseArgsToListOfTuples(
            {
                'minItems': 2,
                'maxItems': 3,
                'allowDict': True,
                'allowList': True,
                'allowedDataTypes': (
                    (str, unicode),
                    (str, unicode, int, long, float, bool, list, tuple),
                    (int,)
                ),
            },
            *args,
            **kwds
        ):
            condition = self._conditionObject()
            condition.set(column, value, relation)
            if condition not in self:
                self._conditions.append(condition)
        
        return self
    
    def remove(self, *keys):
        """
        Remove condition(s).
        """
        if len(keys) == 0:
            self._conditions = []
        
        if not isinstance(keys, (list, tuple)):
            keys = (keys,)
        
        conditions = []
        for condition in self._conditions:
            if condition._column not in keys:
                conditions.append(condition)
        self._conditions = conditions

