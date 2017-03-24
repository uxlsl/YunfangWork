# -*- coding:utf-8 -*-

from django_pandas.io import read_frame

from house.models import (
#        HouseofferforsaleHistory,
        HouseofferforsaleHistoryCopy,
        ResidentialareaAvgPrice)


def residential_stat():
    df = read_frame(HouseofferforsaleHistoryCopy.objects.filter(housetype='普通公寓').only(
        'city',
        'casetime',
        'housetype',
        'residentialareaid',
        'unitprice'))
    df['unitprice'] = df['unitprice'].astype(float)
    g = df.groupby(['city','casetime', 'housetype', 'residentialareaid'])['unitprice'].mean()

    for k,v in g.iteritems():
        ResidentialareaAvgPrice.objects.update_or_create(
                type=k[2],
                chengShi=k[0],
                ShiJian=k[1],
                residentialareaid=k[3],
                defaults={'junJia':v}
                )
