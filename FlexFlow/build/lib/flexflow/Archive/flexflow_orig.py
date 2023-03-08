#!/usr/bin/env python
"""
API to interact with FFTesterWebService

Joe Merle for Centos7 Linux Customer: PureStorage
19-Jan-2017

Last update: 26-Jan-2017 09:15
Cleaned up unused variables and fixed bug with strStationName vs. strStation

"""

import sys
import datetime
import getopt
from xml.dom import minidom
from suds.sax.text import Raw
from suds.client import Client
#import pprint #just for debug

#var=input("Please enter a SN: ") 

def wsGetUnitInfo(URLService=None, strRequest=None, strStationName=None, strUserID=None, strUnitInfo=None): #good 20160603
    """ Calls GetUnitInfo for a given unit serial number

    Args:
        URLService: the url for the web service
        strRequest: Unit identificator. Must be a available value in ffserialnumber.value in the FF instance pointed by the web service (see config.ini on the web service folder on the server)
        strStationName: Physical station name according to Flexflow, i.e. HWvalidation
        strUserID: any valid FF user; default value is admin
        strUnitInfo: should be None

    Returns:
        UnitReadyForTest: True if GetUnitInfoResponse.GetUnitInfoResult=0, otherwise False;
		python -c "import FFStarryTester; FFStarryTester.wsGetUnitInfo('http://aurnt501/FFTesterWSProd/FFTesterWS.asmx?WSDL','DailyHipotSN','L1-Fridge_Hipot-1','admin')"
    """
    
    if URLService is None:
        raise ValueError("URLService cannot be emtpy")

    if strRequest is None:
        raise ValueError("strRequest cannot be emtpy")

    if strStationName is None:
        raise ValueError("strStationName cannot be emtpy")

    if strUserID is None:
        strUserID = 'admin'

    UnitReadyForTest = False
    client = Client(URLService)
    GetUnitInfoResponse = client.service.GetUnitInfo(strRequest,strUnitInfo,strStationName,strUserID)
    print GetUnitInfoResponse
    if GetUnitInfoResponse.GetUnitInfoResult == 0:
        UnitReadyForTest = True
        strUnitInfo = GetUnitInfoResponse.strUnitInfo
        #print strUnitInfo
    return UnitReadyForTest


def wsSaveResult(URLService=None, strXMLResultText=None, strStationName=None):
    """ Calls SaveResult for a given unit serial number or MAC Address

    Args:
        URLService: the url for the web service, i.e.: "http://sacnte939/WSFFTesterCiii/FFTesterWS.asmx?WSDL"
        strXMLResultText: XML string with test result information
        strStationName: Physical station name according to Flexflow; Defatul value is HWValidation

    Returns:
        iResponse: 0 if successful, <> 0 otherwise
    """
    if URLService is None:
        raise ValueError("strXMLResultText cannot be emtpy")

    if strXMLResultText is None:
        raise ValueError("strXMLResultText cannot be emtpy")

    if strStationName is None:
        raise ValueError("strXMLResultText cannot be emtpy")

    client = Client(URLService)
    print 'strXMLResultText is \n', strXMLResultText
    iResponse = client.service.SaveResult(strXMLResultText, strStationName)

    if not iResponse is None:
        # pp = pprint.PrettyPrinter(indent=4) #TODO: Remove this line
        # pp.pprint(strUnitInfo) #TODO: Remove this line
        return iResponse
    else:
        return


def createXMLTestResult(UUTID=None, strStationName=None, strUserID=None, strTestResult=None, strSymptom=None,
                        strTestStart=None, strTestTime=None):
    """Create the XML that will be passed to FF via WS based on the test results available on a flat file.
    Args:
        UUTID: Serial Number (SN) of the UUT. This SN has to be available as a Unit in FF.
        strTestResult: Only valid values are PASSED or FAILED indicating the test result (AVT or FT)
        strFileName: For future use. The intention is to read the difference found during AVT and/or results from FT to then form strXMLResult.

    Return:
        strXMLResult: string with test results formatted
    """
    strInput = ''

    if UUTID == None:
        raise ValueError("parameter UUTID cannot be empty")
    if strStationName == None:
        raise ValueError("parameter strStationName cannot be empty")
    if strUserID == None:
        raise ValueError("parameter strUserID cannot be empty")
    if strTestResult == None:
        raise ValueError("parameter strTestResult cannot be empty")

    if strSymptom == None:
        if strTestResult == 'Passed':
            strSymptom = 'PASSED'
        else:
            strSymptom = 'NONE'
    if strTestStart == None:
        strTestStart = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    if strTestTime == None:
        strTestTime = '0.000000'

    strInput = '''<![CDATA[<BATCH xmlns="http://www.flextronics.com/fts/sfs/res" TIMESTAMP="" SYNTAX_REV="" COMPATIBLE_REV="">'''
    strInput = strInput + '''<FACTORY NAME="" LINE ="" TESTER="'''
    strInput = strInput + strStationName
    strInput = strInput + '''" FIXTURE="" SHIFT="" USER="'''
    strInput = strInput + strUserID
    strInput = strInput + '''" />'''
    strInput = strInput + '''<PRODUCT NAME="" REVISION="" FAMILY="" CUSTOMER="" />'''
    strInput = strInput + '''<REFS SEQ_REF="" FTS_REF="" LIM_REF="" CFG_REF="" CAL_REF="" INSTR_REF="" />'''
    strInput = strInput + '''<PANEL ID="" COMMENT="None" RUNMODE="Production" TIMESTAMP="" TESTTIME="0.000000" WAITTIME="0.000000" STATUS="'''
    strInput = strInput + strTestResult
    strInput = strInput + '''"><DUT ID="'''
    strInput = strInput + UUTID
    # Next line date and test time used by FF
    strInput = strInput + '''" COMMENT="" PANEL="0" SOCKET="0" TIMESTAMP="'''
    strInput = strInput + strTestStart
    strInput = strInput + '''" TESTTIME="'''
    strInput = strInput + strTestTime
    strInput = strInput + '''" STATUS="'''
    strInput = strInput + strTestResult
    strInput = strInput + '''"><GROUP NAME="AutoAVT" STEPGROUP="AutoAVT" GROUPINDEX="1" LOOPINDEX="0" TYPE="" RESOURCE="FFTesterInterface.py" MODULETIME="0" TOTALTIME="0" TIMESTAMP="'''
    strInput = strInput + strTestStart
    strInput = strInput + '''" STATUS="'''
    strInput = strInput + strTestResult
    strInput = strInput + '''">'''
    # Result after Header
    strInput = strInput + '''<TEST NAME="'''
    strInput = strInput + strStationName
    strInput = strInput + '''" DESCRIPTION="'''
    strInput = strInput + strSymptom
    strInput = strInput + '''" UNIT="" VALUE="" HILIM="" LOLIM="" STATUS="'''
    strInput = strInput + strTestResult
    strInput = strInput + '''" RULE="NONE" TARGET="" DATATYPE="Number"/>'''
    # Footer
    strInput = strInput + '''</GROUP></DUT></PANEL></BATCH>]]>'''
    strXMLResult = Raw(strInput)
    return strXMLResult
