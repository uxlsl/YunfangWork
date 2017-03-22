# -*- coding:utf-8 -*-
from house.models import HouseofferforsaleHistory

from house.models import AuxiliaryNotFound
from django.db import connections


def run():
    con = connections['auxiliary']
    cursor = con.cursor()
    cursor.execute('show tables')
    tables = cursor.fetchall()
    info = {}
    for tablename, in tables:
        sql='select 中介人,联系电话,中介机构,中介门店,对应中介机构,对应中介门店 from {}'.format(tablename)
        cursor.execute(sql)
        for i in cursor.fetchall():
            if 'NULL' in i:
                continue
            a,b,c,d = i[:4]
            d = d.replace(c, '')
            k = (a, b, c, d)
            y = tuple(i[4:])
            info[k] = y

    for h in HouseofferforsaleHistory.objects.all():
        if h.agency is None or h.agentstores is None:
            continue
        agentstores = h.agentstores.replace(h.agency, '')
        agentstores = agentstores.replace('.', '')
        k = (h.agentname, h.agenttelephone, h.agency, agentstores)
        if k in info:
            h.correspondagent, h.correspondagentstores = info[k]
            h.save()

        AuxiliaryNotFound.objects.update_or_create(
                agentname=h.agentname,
                agenttelephone=h.agenttelephone,
                agency=h.agency,
                agentstores=h.agentstores)

