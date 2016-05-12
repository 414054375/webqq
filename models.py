#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lsqlite import db
from lsqlite.orm import Model, StringField, BooleanField, FloatField, TextField,IntegerField
import config
def raw_choose(message):
    choose = raw_input(message + ' [y/n]')
    return choose.strip().lower() in ['y', 'yes']

class UserTable(Model):
    __table__ = 'user'

    ID = IntegerField(primary_key=True, updatable=False, ddl='varchar(20)')
    password = StringField(ddl='varchar(15)')
    nickname = StringField(ddl='varchar(15)')

    @classmethod
    def query(self,id):
        return db.select("select * from user where ID = ?", id)

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if raw_choose('Initialize all the table in %s?' % config.database):
        L = []
        L.append(UserTable)
        db.create_engine(config.database);
        for m in L:
            db.update('drop table if exists %s' % m.__table__)
            db.update(m().__sql__())
        gty = UserTable(ID = 10000,password = "19950305",nickname = "administrator")
        gty.insert()