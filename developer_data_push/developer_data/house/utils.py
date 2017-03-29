# -*- coding:utf-8 -*-

from house.models import HouseofferforsaleHistory

from house.models import AuxiliaryNotFound
from django.db import connections


def feed_agent():
    con = connections['auxiliary']
    cursor = con.cursor()
    cursor.execute('show tables')
    tables = cursor.fetchall()
    info = {}
    for tablename, in tables:
        sql='select 来源,中介人,联系电话,中介机构,中介门店,对应中介机构,对应中介门店 from {}'.format(tablename)
        cursor.execute(sql)
        for i in cursor.fetchall():
            if 'NULL' in i:
                continue
            a,b,c,d,e = i[:5]
            e = e.replace(d, '')
            k = (a, b, c, d, e)
            y = tuple(i[5:])
            info[k] = y
    count = 0
    total = HouseofferforsaleHistory.objects.filter(casefrom='安居客').count()
    for h in HouseofferforsaleHistory.objects.filter(casefrom='安居客'):
        if h.agency is None or h.agentstores is None:
            continue
        agentstores = h.agentstores.replace(h.agency, '')
        agentstores = agentstores.replace('.', '')
        k = (h.casefrom, h.agentname, h.agenttelephone, h.agency, agentstores)
        if k in info:
            h.correspondagent, h.correspondagentstores = info[k]
            h.save()
            count += 1

        AuxiliaryNotFound.objects.update_or_create(
                casefrom=h.casefrom,
                agentname=h.agentname,
                agenttelephone=h.agenttelephone,
                agency=h.agency,
                agentstores=h.agentstores)

    return total, count
