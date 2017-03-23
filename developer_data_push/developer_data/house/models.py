# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class HouseofferforsaleHistory(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=64, blank=True, null=True)  # Field name made lowercase.
    housename = models.CharField(db_column='HouseName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    districtname = models.CharField(db_column='DistrictName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    specialfactor = models.CharField(db_column='SpecialFactor', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    residentialareaname = models.CharField(db_column='ResidentialAreaName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    casetime = models.DateTimeField(db_column='CaseTime', blank=True, null=True)  # Field name made lowercase.
    casefrom = models.CharField(db_column='CaseFrom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sourceid = models.CharField(db_column='SourceID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sourcemeta = models.TextField(db_column='SourceMeta', blank=True, null=True)  # Field name made lowercase.
    sourcelink = models.CharField(db_column='SourceLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sourcetitle = models.CharField(db_column='SourceTitle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    supplementary = models.CharField(db_column='Supplementary', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    extdata = models.TextField(db_column='ExtData', blank=True, null=True)  # Field name made lowercase.
    buildingcategory = models.CharField(db_column='BuildingCategory', max_length=100, blank=True, null=True)  # Field name made lowercase.
    buildingcompletedyear = models.IntegerField(db_column='BuildingCompletedYear', blank=True, null=True)  # Field name made lowercase.
    remainyear = models.IntegerField(db_column='RemainYear', blank=True, null=True)  # Field name made lowercase.
    buildingarea = models.DecimalField(db_column='BuildingArea', max_digits=19, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    insideofbuildingarea = models.DecimalField(db_column='InsideOfBuildingArea', max_digits=19, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    toward = models.CharField(db_column='Toward', max_length=100, blank=True, null=True)  # Field name made lowercase.
    decoration = models.CharField(db_column='Decoration', max_length=255, blank=True, null=True)  # Field name made lowercase.
    housenature = models.CharField(db_column='HouseNature', max_length=100, blank=True, null=True)  # Field name made lowercase.
    housetype = models.CharField(db_column='HouseType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    realusetype = models.CharField(db_column='RealUseType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    supportingfacility = models.TextField(db_column='SupportingFacility', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=19, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.DecimalField(db_column='TotalPrice', max_digits=19, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    categoryofproperty = models.CharField(db_column='CategoryofProperty', max_length=150, blank=True, null=True)  # Field name made lowercase.
    zonecasefrom = models.CharField(db_column='ZoneCaseFrom', max_length=100, blank=True, null=True)  # Field name made lowercase.
    partition = models.CharField(db_column='Partition', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dwelling = models.CharField(db_column='Dwelling', max_length=150, blank=True, null=True)  # Field name made lowercase.
    housetags = models.CharField(db_column='HouseTags', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unitshape = models.CharField(db_column='UnitShape', max_length=255, blank=True, null=True)  # Field name made lowercase.
    unitstructure = models.CharField(db_column='UnitStructure', max_length=150, blank=True, null=True)  # Field name made lowercase.
    rooms = models.IntegerField(db_column='Rooms', blank=True, null=True)  # Field name made lowercase.
    halls = models.IntegerField(db_column='Halls', blank=True, null=True)  # Field name made lowercase.
    kitchens = models.IntegerField(db_column='Kitchens', blank=True, null=True)  # Field name made lowercase.
    toilets = models.IntegerField(db_column='Toilets', blank=True, null=True)  # Field name made lowercase.
    balconys = models.IntegerField(db_column='Balconys', blank=True, null=True)  # Field name made lowercase.
    agency = models.CharField(db_column='Agency', max_length=255, blank=True, null=True)  # Field name made lowercase.
    correspondagent = models.CharField(db_column='CorrespondaAgency', max_length=255, blank=True, null=True, verbose_name='对应中介机构')  # Field name made lowercase.
    agentname = models.CharField(db_column='AgentName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agenttelephone = models.CharField(db_column='AgentTelephone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    agentstores = models.CharField(db_column='AgentStores', max_length=255, blank=True, null=True)  # Field name made lowercase.
    correspondagentstores = models.CharField(db_column='CorrespondaAgentStores', max_length=255, blank=True, null=True, verbose_name='对应中介门店')  # Field name made lowercase.
    housespictures = models.CharField(db_column='HousesPictures', max_length=6000, blank=True, null=True)  # Field name made lowercase.
    floorname = models.CharField(db_column='FloorName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    floor = models.IntegerField(db_column='Floor', blank=True, null=True)  # Field name made lowercase.
    floors = models.IntegerField(db_column='Floors', blank=True, null=True)  # Field name made lowercase.
    floorcount = models.IntegerField(db_column='FloorCount', blank=True, null=True)  # Field name made lowercase.
    floortype = models.CharField(db_column='FloorType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sharedpublicarea = models.DecimalField(db_column='SharedPublicArea', max_digits=19, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    unitstructureflag = models.IntegerField(db_column='UnitStructureFlag', blank=True, null=True)  # Field name made lowercase.
    housetypeflag = models.IntegerField(db_column='HouseTypeFlag', blank=True, null=True)  # Field name made lowercase.
    lastcasetime = models.DateTimeField(db_column='LastCaseTime', blank=True, null=True)  # Field name made lowercase.
    casecount = models.IntegerField(db_column='CaseCount', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255, blank=True, null=True)  # Field name made lowercase.
    residentialareaid = models.IntegerField(db_column='ResidentialAreaID', blank=True, null=True)  # Field name made lowercase.
    buildingid = models.IntegerField(db_column='BuildingID', blank=True, null=True)  # Field name made lowercase.
    unitid = models.IntegerField(db_column='UnitID', blank=True, null=True)  # Field name made lowercase.
    houseid = models.IntegerField(db_column='HouseID', blank=True, null=True)  # Field name made lowercase.
    modifydate = models.DateTimeField(db_column='ModifyDate', blank=True, null=True)  # Field name made lowercase.
    tguid = models.CharField(db_column='TGuid', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    expansion = models.TextField(db_column='Expansion', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(max_length=255, blank=True, null=True)
    oppositeid = models.CharField(db_column='oppositeId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    crawlat = models.CharField(db_column='crawlAt', max_length=50, blank=True, null=True)  # Field name made lowercase.
    housingdatatype = models.CharField(db_column='housingDataType', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'houseofferforsale_history'


class AuxiliaryNotFound(models.Model):
    agentname = models.CharField(db_column='AgentName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agenttelephone = models.CharField(db_column='AgentTelephone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    agency = models.CharField(db_column='Agency', max_length=255, blank=True, null=True)  # Field name made lowercase.
    agentstores = models.CharField(db_column='AgentStores', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="备份时间")
