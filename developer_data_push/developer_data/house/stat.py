# -*- coding:utf-8 -*-
import pandas as pd
from django_pandas.io import read_frame
from house.models import (
        HouseofferforsaleHistory,
        HouseofferforsaleHistoryCopy,
        ResidentialareaAvgPrice,
        AgentStat
        )


def residential_stat():
    """小区均价统计
    """
    df = read_frame(HouseofferforsaleHistoryCopy.objects.filter(casetime__gte='2017-03-01 00:00:00', housetype__contains='公寓').only(
    #df = read_frame(HouseofferforsaleHistoryCopy.objects.all().only(
        'city',
        'casetime',
        'housetype',
        'residentialareaid',
        'unitprice'))
    df['unitprice'] = df['unitprice'].astype(float)
    g = df.groupby(['city','casetime', 'housetype', 'residentialareaid'])['unitprice'].mean()

    for k,v in g.iteritems():
        print(k)
        ResidentialareaAvgPrice.objects.update_or_create(
                type=k[2],
                chengShi=k[0],
                ShiJian=k[1],
                residentialareaid=k[3],
                defaults={'junJia':v}
                )


def agent_stat():
    df = read_frame(HouseofferforsaleHistoryCopy.objects.filter(casetime__gte='2017-03-01 00:00:00'))
    #df = read_frame(HouseofferforsaleHistoryCopy.objects.all())
    def f(x):
        return pd.Series({
            'agentstore_count': len(x['agentstores'].unique()),
            'agentname_count': len(x['agentname'].unique()),
            'house_count': len(x)})
    total = 0
    results = df.groupby(['casetime', 'city', 'districtname','residentialareaname','agency', 'unitshape']).apply(f)

    lst = []
    for index, row in results.iterrows():
        item = []
        item.extend(index)
        item.extend([row['agentstore_count'], row['agentname_count'], row['house_count']])
        print(item)
        lst.append(AgentStat(
                ShiJian=item[0],
                ChengShi=item[1],
                XingZhengQu=item[2],
                PianQu=item[3],
                ZhongJieMingCheng=item[4],
                YeTai=item[5],
                MenDianShu=item[6],
                JingJiRenShu=item[7],
                XinZengGongYingShu=item[8],
                ))
    AgentStat.objects.bulk_create(lst)
    print("end")
    return total,df.count()
