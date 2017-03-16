#coding=utf-8

from sqlalchemy.types import Integer,FLOAT,DECIMAL,DateTime,String

type_map = {
    'int': Integer,
    'float': FLOAT,
    'decimal': DECIMAL,
    'date': DateTime,
    'string': String(2048)
}