# -*- coding:utf-8 -*-
import pandas as pd
from django.core.paginator import Paginator
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


def agent_stat():
    def f(x):
        return pd.Series({
            'agentstore_count': len(x['agentstores'].unique()),
            'agentname_count': len(x['agentname'].unique()),
            'house_count': len(x)})

    fieldnames = (
                'casetime', 'city', 'districtname',
                'residentialareaname','agency', 'housetype',
                'agentstores', 'agentname')

    lst = []
    paginator = Paginator(HouseofferforsaleHistoryCopy.objects.all().only(*fieldnames), 100000)
    for page_idx in range(1, paginator.num_pages):
        print('正在处理第{}页'.format(page_idx))
        object_list = paginator.page(page_idx).object_list
        df = object_list.to_dataframe(fieldnames=fieldnames)
        lst.append(df.groupby(['casetime', 'city', 'districtname','residentialareaname','agency', 'housetype']).apply(f))
        del object_list

    results = None
    for i in lst:
        if i.empty:
            continue
        if results is None:
            results = i
        else:
            results += i

    if results.empty:
        return

    for index, row in results.iterrows():
        item = []
        item.extend(index)
        item.extend([row['agentstore_count'], row['agentname_count'], row['house_count']])
        AgentStat.objects.update_or_create(
                ShiJian=item[0],
                ChengShi=item[1],
                XingZhengQu=item[2],
                PianQu=item[3],
                ZhongJieMingCheng=item[4],
                YeTai=item[5],
                defaults={
                    'MenDianShu':item[6],
                    'JingJiRenShu':item[7],
                    'XinZengGongYingShu':item[8],
                    })

    return
