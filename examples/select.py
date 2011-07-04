#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle


print sqlpuzzle.select().from_('table')
# output: SELECT * FROM `table`

print sqlpuzzle.selectFrom('table')
# same output as previous command


sql = sqlpuzzle.select('id', 'name')
sql.from_('table')
sql.columns(('first_name', 'firstName')) # tuple is for AS
sql.from_('table2')
print sql
# output:
# SELECT `id`, `name`, `first_name` AS "firstName" FROM `table`, `table2`
