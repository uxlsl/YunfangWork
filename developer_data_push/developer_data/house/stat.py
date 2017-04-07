# -*- coding:utf-8 -*-
import datetime
import pandas as pd
from django_pandas.io import read_frame
from house.models import (
        HouseofferforsaleHistory,
        ResidentialareaAvgPrice,
        AgentStat
        )


def residential_stat_range(start, end):
    """小区均价统计
    """
    df = read_frame(HouseofferforsaleHistory.objects.filter(
        casetime__gte=start,
        casetime__lt=end,
        housetype__contains='公寓').only(
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


def residential_stat(start, end, step=datetime.timedelta(days=5)):
    """
    小区均价统计
    """
    s = start
    e = s + step
    while s < end:
        residential_stat_range(s, e)
        s,e = e, e+step


def agent_stat_range(start, end):
    print("进行中介统计 {}-{}".format(start, end))
    df = read_frame(HouseofferforsaleHistory.objects.filter(casetime__gte=start, casetime__lt=end))
    #df = read_frame(HouseofferforsaleHistoryCopy.objects.all())
    def f(x):
        return pd.Series({
            'agentstore_count': len(x['agentstores'].unique()),
            'agentname_count': len(x['agentname'].unique()),
            'house_count': len(x)})
    total = 0
    results = df.groupby(['casetime', 'city', 'districtname','residentialareaname','agency', 'housetype']).apply(f)

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
    AgentStat.objects.filter(ShiJian__gte=start, ShiJian__lt=end).delete()
    AgentStat.objects.bulk_create(lst)
    return total,df.count()


def agent_stat(start, end, step=datetime.timedelta(days=1)):
    s = start
    e = s + step
    while s < end:
        agent_stat_range(s, e)
        s,e = e, e+step
