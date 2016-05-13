#coding:utf-8

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

def New_Friend_Table(id):#########################GTY神界护体###############################
    class FriendTable(Model):
        __table__ = 'F'+str(id)#定义表名 比如10000F
        ID= IntegerField(primary_key=True,updatable=False,ddl='varchar(20)')
        Status = StringField(ddl='varchar(1)')#status表示状态 Y为已经是好友 A表示其他人有好友申请等待审核
    return FriendTable

def Check_Friend_Table(id):
    return db.select("select count(*) from sqlite_master where type='table' and name = ?","F"+str(id))[0]["count(*)"] 

def Get_Friends(id):
    a = db.select("select ID from %s" % 'F'+str(id))
    id_list = []
    for i in a:
        id_list.append(i["ID"])
    return id_list

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if raw_choose('Initialize all the table in %s?' % config.database):
        L = []
        L.append(UserTable)
        #L.append(FriendTable)

        db.create_engine(config.database);
        for m in L:
            db.update('drop table if exists %s' % m.__table__)
            db.update(m().__sql__())
        UserTable(ID = 10000,password = "123456",nickname = u"龙傲天").insert()
        UserTable(ID = 10001,password = "123456",nickname = u"龙傲天2").insert()
        #插入好友列表
        b = New_Friend_Table(10000)(ID = 10001,Status = "Y")
        b.insert()
        #FriendTable(ID = 10001,Status = "Y").insert()