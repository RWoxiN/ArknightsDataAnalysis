# -*- coding: utf-8 -*-
from peewee import *
from .config import ada_config

database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class Account(BaseModel):
    uid = CharField(max_length=20, unique=True)
    nickname = CharField(max_length=50)
    token = CharField(max_length=50)

class OSRPool(BaseModel):
    name = CharField(max_length=20, unique=True)
    type = CharField()

class OperatorSearchRecord(BaseModel):
    account = ForeignKeyField(Account, backref='records')
    time = DateTimeField()
    pool = ForeignKeyField(OSRPool, backref='records')

class OSROperator(BaseModel):
    name = CharField(max_length=10)
    rarity = IntegerField()
    is_new = BooleanField()
    index = IntegerField()
    record = ForeignKeyField(OperatorSearchRecord, backref='operators')

class PayRecord(BaseModel):
    name = CharField()
    pay_time = DateTimeField()
    account = ForeignKeyField(Account, backref='pay_records')
    platform = CharField()
    order_id = CharField(unique=True)
    amount = IntegerField()

a_config = ada_config()
database_type, database_type_config = a_config.load_config_database()
if database_type == 'sqlite3':
    db_name = database_type_config.get('filename')
    db = SqliteDatabase(db_name)
if database_type == 'mysql':
    db_host = database_type_config.get('host')
    db_user = database_type_config.get('user')
    db_pass = database_type_config.get('password')
    db_name = database_type_config.get('database')
    db = MySQLDatabase(db_name, host=db_host, user=db_user, passwd=db_pass, port=3306)
database_proxy.initialize(db)
database_proxy.create_tables([Account, OSRPool, OperatorSearchRecord, OSROperator, PayRecord])
