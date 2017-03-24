# -*- coding:utf-8 -*-

from django.db import connections
from house.models import HouseofferforsaleHistoryCopy


def run():
    con = connections['basehouse']
    cursor = con.cursor()
    cursor.execute('show tables')
    tables = [i[0] for i in cursor.fetchall()]
    total = 0

    for i in tables:
        cursor.execute('select * from {}'.format(i))

        lst = []

        for j in cursor.fetchall():
            total += 1
            h = HouseofferforsaleHistoryCopy(
                    city=j[0],
                    districtname=j[1],
                    zonecasefrom=j[2],
                    residentialareaid=j[3],
                    residentialareaname=j[4],
                    casetime=j[7],
                    unitshape=j[8],
                    dwelling=j[9],
                    buildingarea=j[10],
                    buildingcompletedyear=j[11],
                    unitprice=j[12],
                    totalprice=j[13],
                    )
            lst.append(h)
            if len(lst) >= 1000:
                HouseofferforsaleHistoryCopy.objects.bulk_create(lst)
                lst = []
            print(total)

        if len(lst) > 0:
            HouseofferforsaleHistoryCopy.objects.bulk_create(lst)

