# -*- coding: utf-8 -*-


import conditions
import limit


SELECT = 1
INSERT = 2
UPDATE = 3


class SqlPuzzle:
    def __init__(self):
        """
        Initialization of SqlPuzzle.
        """
        self.__sqlType = None
        self.__tables = None
        self.__columns = None
        self.__values = None
        self.__conditions = conditions.Conditions()
        self.__limit = limit.Limit()
    
    def __setSqlType(self, type_):
        assert type_ is not None, 'You can\'t change type of query.'
        assert type_ in (SELECT, INSERT, UPDATE), 'Type \'%s\' of query is undefind.' % type_
        self.__sqlType = type_
    
    # SELECT
    
    def select(self, *columns):
        """
        Set column(s) to select.
        """
        self.__setSqlType(SELECT)
        self.__columns = columns
        return self
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self.__tables = tables
        return self
    
    def limit(self, limit, offset=None):
        """
        Set limit (and offset).
        """
        self.__limit.limit(limit, offset)
        return self
    
    def offset(self, offset):
        """
        Set offset.
        """
        self.__limit.offset(offset)
        return self
    
    # INSERT
    
    def insert(self):
        """
        Set query to insert.
        """
        self.__setSqlType(INSERT)
        return self
    
    def into(self, table):
        """
        Set table for insert.
        """
        self.__tables = [table]
        return self
    
    def insertInto(self, table):
        """
        Set query to insert.
        """
        return self.insert().into(table)
    
    def values(self, *args, **kwargs):
        """
        Set columns and values.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self.__columns = args[0].keys()
            self.__values = args[0].values()
        elif kwargs is not None:
            self.__columns = kwargs.keys()
            self.__values = kwargs.values()
        else:
            raise 'Values can be dictionary or keyworded variable arguments.'
        return self
    
    # UPDATE
    
    def update(self, table):
        """
        Set table for update.
        """
        self.__setSqlType(UPDATE)
        self.__tables = [table]
        return self
    
    def set(self, *args, **kwargs):
        """
        Set columns and values.
        """
        self.values(*args, **kwargs)
        return self
    
    # WHERE
    
    def where(self, *args, **kwargs):
        """
        Set condition(s) to query.
        """
        self.__conditions.where(*args, **kwargs)
        return self
    
    # PRINT
    
    def __str__(self):
        """
        Print query.
        """
        return self.getQuery()
    
    def getQuery(self):
        """
        Generate query.
        """
        if self.__sqlType == SELECT:
            return self.__generateSelect()
        elif self.__sqlType == INSERT:
            return self.__generateInsert()
        elif self.__sqlType == UPDATE:
            return self.__generateUpdate()
        raise 'Not implemented for sql type %s.' % self.__sqlType
    
    # GENERATE
    
    def __generateSelect(self):
        """
        Generate SELECT.
        """
        select = "SELECT %s FROM %s" % (
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('`%s`' % table for table in self.__tables)),
        )
        if self.__conditions.isSet(): select = "%s %s" % (select, self.__conditions)
        if self.__limit.isSet(): select = "%s %s" % (select, self.__limit)
        
        return select
    
    def __generateInsert(self):
        """
        Generate INSERT.
        """
        assert len(self.__tables) == 1, 'INSERT must have only one table.'
        assert not self.__conditions.isSet(), 'INSERT does not have WHERE.'
        
        insert = "INSERT INTO `%s` (%s) VALUES (%s)" % (
            self.__tables[0],
            ', '.join(('`%s`' % column for column in self.__columns)),
            ', '.join(('"%s"' % value for value in self.__values)),
        )
        return insert
    
    def __generateUpdate(self):
        """
        Generate UPDATE.
        """
        assert len(self.__tables) == 1, 'INSERT must have only one table.'
        
        update = "UPDATE `%s` SET %s" % (
            self.__tables[0],
            ', '.join(('`%s` = "%s"' % (column, value) for column, value in zip(self.__columns, self.__values)))
        )
        if self.__conditions.isSet(): update = "%s %s" % (update, self.__conditions)
        
        return update

