# -*- coding:utf-8 -*-

from django.db import connection

sql = """
INSERT INTO `{}` (`Tid`, `City`, `HouseName`, `DistrictName`, `SpecialFactor`, `ResidentialAreaName`, `Address`, `CaseTime`, `CaseFrom`, `SourceID`, `SourceMeta`, `SourceLink`, `SourceTitle`, `Supplementary`, `ExtData`, `BuildingCategory`, `BuildingCompletedYear`, `RemainYear`, `BuildingArea`, `InsideOfBuildingArea`, `Toward`, `Decoration`, `HouseNature`, `HouseType`, `RealUseType`, `SupportingFacility`, `UnitPrice`, `TotalPrice`, `CategoryofProperty`, `ZoneCaseFrom`, `Partition`, `Dwelling`, `HouseTags`, `UnitShape`, `UnitStructure`, `Rooms`, `Halls`, `Kitchens`, `Toilets`, `Balconys`, `Agency`, `CorrespondaAgency`, `AgentName`, `AgentTelephone`, `AgentStores`, `CorrespondaAgentStores`, `HousesPictures`, `FloorName`, `Floor`, `Floors`, `FloorCount`, `FloorType`, `SharedPublicArea`, `UnitStructureFlag`, `HouseTypeFlag`, `LastCaseTime`, `CaseCount`, `Comment`, `ResidentialAreaID`, `BuildingID`, `UnitID`, `HouseID`, `ModifyDate`, `TGuid`, `PID`, `Expansion`, `CreatedDate`, `Status`, `remark`, `oppositeId`, `crawlAt`, `housingDataType`, `HouseStatus`, `datadate`)

SELECT `Tid`, `City`, `HouseName`, `DistrictName`, `SpecialFactor`, `ResidentialAreaName`, `Address`, `CaseTime`, `CaseFrom`, `SourceID`, `SourceMeta`, `SourceLink`, `SourceTitle`, `Supplementary`, `ExtData`, `BuildingCategory`, `BuildingCompletedYear`, `RemainYear`, `BuildingArea`, `InsideOfBuildingArea`, `Toward`, `Decoration`, `HouseNature`, `HouseType`, `RealUseType`, `SupportingFacility`, `UnitPrice`, `TotalPrice`, `CategoryofProperty`, `ZoneCaseFrom`, `Partition`, `Dwelling`, `HouseTags`,
`UnitShape`, `UnitStructure`, `Rooms`, `Halls`, `Kitchens`, `Toilets`, `Balconys`, `Agency`, `CorrespondaAgency`, `AgentName`, `AgentTelephone`, `AgentStores`, `CorrespondaAgentStores`, `HousesPictures`, `FloorName`, `Floor`, `Floors`, `FloorCount`, `FloorType`, `SharedPublicArea`, `UnitStructureFlag`, `HouseTypeFlag`, `LastCaseTime`, `CaseCount`, `Comment`, `ResidentialAreaID`, `BuildingID`, `UnitID`, `HouseID`, `ModifyDate`, `TGuid`, `PID`, `Expansion`, `CreatedDate`, `Status`, `remark`,
`oppositeId`, `crawlAt`, `housingDataType`, `HouseStatus`, `datadate` FROM `houseofferforsale_history_copy`
"""

def run():
    lst = [
            #'houseofferforsale_history_beijing',
            'houseofferforsale_history_tianjin',
            #'houseofferforsale_history_zhengzhou'
            ]

    cursor = connection.cursor()

    for i in lst:
        print(sql.format(i))
        cursor.execute(sql.format(i))
        print(cursor.fetchall())
