import xml.etree.ElementTree as ET
import json
from os import listdir
import re

data_parsed_dic = []
data_parsed_dic_by_row = {}
seatTypesIdsListForEachSeatId = {}
seatTypesIdsDefinitionListForEachSeatId = {}
seatTypesIdsDefinitionList = {}


def createSeatObj():
    for filename in listdir('./'):
        if filename.endswith('.xml') or filename.endswith('.XML'):
            with open(filename, 'r', encoding="utf-8") as content:
                tree = ET.parse(content)
                root = tree.getroot()
                ns = {"ns": "http://www.opentravel.org/OTA/2003/05/common/", "ns2": "http://www.iata.org/IATA/EDIST/2017.2"}
                if (filename == "seatmap1.xml"):
                    for row in root.findall(".//ns:RowInfo", ns):
                        for elm in row.findall(".//ns:SeatInfo", ns):
                            obj = {}
                            obj["seat-id"] = elm[0].attrib["SeatNumber"]
                            obj["availability"] = elm[0].attrib["AvailableInd"]
                            obj["cabin-class"]= row.attrib["CabinType"]
                            if (elm[0].attrib["AvailableInd"] == "true"):
                                serviceTagIndex = len(elm) - 1
                                obj["seat-price"] = f"{elm[serviceTagIndex][0].attrib['Amount']} {elm[serviceTagIndex][0].attrib['CurrencyCode']}"
                            else:
                                obj["seat-price"] = ""
                            data_parsed_dic.append(obj)
                else:
                    for row in root.findall(".//ns2:Row", ns):
                        for seat in row.findall(".//ns2:Seat", ns):
                            seatId = f"{row[0].text}{seat[0].text}"
                            seatTypesIdsListForEachSeatId[f"{seatId}"] = []
                            for seatDef in seat.findall(".//ns2:SeatDefinitionRef", ns):
                                seatTypesIdsListForEachSeatId[f"{seatId}"].append(seatDef.text)

                    for seatDef in root.findall(".//ns2:SeatDefinition", ns):
                        seatDefId = seatDef.attrib["SeatDefinitionID"]
                        seatTypesIdsDefinitionList[f"{seatDefId}"] = seatDef[0][0].text

                    for seatId in seatTypesIdsListForEachSeatId:
                        seatTypesIdsList = seatTypesIdsListForEachSeatId[seatId]
                        seatTypesIdsListDefinitions = []
                        for seatTypeId in seatTypesIdsList:
                            seatTypesIdsListDefinitions.append(seatTypesIdsDefinitionList[seatTypeId])
                        seatTypesIdsDefinitionListForEachSeatId[seatId] = seatTypesIdsListDefinitions


    for seatDic in data_parsed_dic:
        if (seatDic["seat-id"] in seatTypesIdsDefinitionListForEachSeatId):
            seatDic["seat-type"] = seatTypesIdsDefinitionListForEachSeatId[seatDic["seat-id"]]
        else:
            seatDic["seat-type"] = ""

def getRowNumberFromSeatId(seatDic):
    splittedSeatId = re.split(r'(\d+)', seatDic["seat-id"])
    rowNumber = splittedSeatId[1]
    return rowNumber

def createObjectWithRowNumberAsKeyAndItsSeatObjectsAsValue():
    for seatDic in data_parsed_dic:
        rowNumber = getRowNumberFromSeatId(seatDic)
        if (rowNumber not in data_parsed_dic_by_row):
            data_parsed_dic_by_row[f"{rowNumber}"] = []
        data_parsed_dic_by_row[f"{rowNumber}"].append(seatDic)


createSeatObj()
createObjectWithRowNumberAsKeyAndItsSeatObjectsAsValue()

with open('./seatmap_parser_parsed.json', 'w') as parsedToJson:
    json.dump(data_parsed_dic_by_row , parsedToJson, indent=4, sort_keys=True)
