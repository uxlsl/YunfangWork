# -*- coding:utf-8 -*-
import pandas as pd
from django_pandas.io import read_frame
from house.models import  HouseofferforsaleHistory, AgentStat


def run():
    df = read_frame(HouseofferforsaleHistory.objects.all())
    def f(x):
        return pd.Series({
            'agentstore_count': len(x['agentstores'].unique()),
            'agentname_count': len(x['agentname'].unique()),
            'house_count': len(x)})
    total = 0
    results = df.groupby(['casetime', 'city', 'districtname','residentialareaname','agency', 'unitshape']).apply(f)
    for index, row in results.iterrows():
        print('#'*30)
        item = (*index, row['agentstore_count'], row['agentname_count'], row['house_count'])
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
        print(item)
        print('#'*30)

    print(df.count())
    print(total)
