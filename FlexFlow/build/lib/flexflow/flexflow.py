#!/usr/bin/env python
"""
API to interact with FFTesterWebService
Written by Jon Mastracchio - TE 

"""
import sys
import datetime
from suds.sax.text import Raw
from suds.client import Client

class flexflow():
	stationName		= '' # 09 - AUTO FCT TEST [430]
	userName		= 'admin' # admin
	URLService		= '' # http://aurnt090/ZeusFFTesterWS/FFTesterWS.asmx?WSDL
	debugMode		= 0
	
	def __init__(self, station, user, server):
		"""
		Ex: flexflow('09 - AUTO FCT TEST [430]','admin','http://aurnt090/ZeusFFTesterWS/FFTesterWS.asmx?WSDL')
		"""
		self.stationName 	= station
		self.userName 		= user 
		self.URLService		= server
		print()
	
	def print_inputs(self):
		print('{:<20} {:<25}'.format('USER:',self.userName))
		print('{:<20} {:<25}'.format('Station:',self.stationName))
		print('{:<20} {:<25}'.format('Serive URL:',self.URLService))
		
	def set_debugMode(self, switch):
		self.debugMode = switch
		print('{:<20} {:<25}'.format('Debug Set to:',self.debugMode))
	
	def wsGetUnitInfo(self, strRequest=None, strUnitInfo=None): #good 20160603
		""" Calls GetUnitInfo for a given unit serial number

		Args:
			self.URLService: the url for the web service
			strRequest: Unit identificator. Must be a available value in ffserialnumber.value in the FF instance pointed by the web service
			self.stationName: Physical station name according to Flexflow
			self.userName: any valid FF user; default value is admin
			strUnitInfo: should be None

		Returns:
			UnitReadyForTest: True if GetUnitInfoResponse.GetUnitInfoResult=0, otherwise False;
		"""
		
		if self.URLService is None:
			raise ValueError("URLService cannot be emtpy")

		if strRequest is None:
			raise ValueError("strRequest cannot be emtpy")

		if self.stationName is None:
			raise ValueError("tationName cannot be emtpy")

		if self.userName is None:
			self.userName = 'admin'

		UnitReadyForTest = False
		client = Client(self.URLService)
		if self.debugMode == 1: print('DEBUG client: {}'.format(client))
		
		GetUnitInfoResponse = client.service.GetUnitInfo(strRequest,strUnitInfo,self.stationName,self.userName)
		if self.debugMode == 1: print('DEBUG GetUnitInfoResponse: {}'.format(GetUnitInfoResponse))
		
		if GetUnitInfoResponse.GetUnitInfoResult == 0:
			UnitReadyForTest = True
			strUnitInfo = GetUnitInfoResponse.strUnitInfo
			#print strUnitInfo
		return UnitReadyForTest, strUnitInfo

	def wsSaveResult(self, strXMLResultText=None):
		""" Calls SaveResult for a given unit serial number or MAC Address

		Args:
			self.URLService: the url for the web service, 
			strXMLResultText: XML string with test result information
			self.stationName: Physical station name according to Flexflow; Defatul value is HWValidation

		Returns:
			iResponse: 0 if successful, <> 0 otherwise
		"""
		if self.URLService is None:
			raise ValueError("URLService cannot be emtpy")

		if strXMLResultText is None:
			raise ValueError("strXMLResultText cannot be emtpy")

		if self.stationName is None:
			raise ValueError("stationName cannot be emtpy")

		client = Client(self.URLService)
		if self.debugMode == 1: print('DEBUG client: {}'.format(client))
		
		#print('strXMLResultText is \n', strXMLResultText)
		iResponse = client.service.SaveResult(strXMLResultText, self.stationName)
		if self.debugMode == 1: print('DEBUG iResponse: {}'.format(iResponse))
		
		if not iResponse is None:
			# pp = pprint.PrettyPrinter(indent=4) #TODO: Remove this line
			# pp.pprint(strUnitInfo) #TODO: Remove this line
			return iResponse
		else:
			return iResponse
			
	def createXMLTestResult(self, UUTID, strTestResult, strTestArray,strScriptName,strSymptom=None,
							strTestStart=None, strTestTime=None, ):
		"""Create the XML that will be passed to FF via WS based on the test results available on a flat file.
		Args:
		UUTID: Serial Number (SN) of the UUT. This SN has to be available as a Unit in FF.
		strTestResult: Only valid values are PASSED or FAILED indicating the test result (AVT or FT)
		strTestArray: Array of test data matching "TEST NAME | RESULT | VALUE | LCL | UCL," Formatting

		Return:
		strXMLResult: string with test results formatted
		"""
		strInput = ''

		if UUTID == None:
			raise ValueError("parameter UUTID cannot be empty")
		if self.stationName == None:
			raise ValueError("parameter self.stationName cannot be empty")
		if self.userName == None:
			raise ValueError("parameter self.userName cannot be empty")
		if strTestResult == None:
			raise ValueError("parameter strTestResult cannot be empty")

		if strSymptom == None:
			if strTestResult == 'PASS':
				strSymptom = 'Passed'
			else:
				strSymptom = 'NONE'
		if strTestStart == None:
			strTestStart = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		if strTestTime == None:
			strTestTime = '0.000000'
			
		if self.debugMode == 1: print('DEBUG StringTestArray: {}'.format(strTestArray))

		strInput = '''<![CDATA[<BATCH xmlns="http://www.flextronics.com/fts/sfs/res" TIMESTAMP="" SYNTAX_REV="" COMPATIBLE_REV="">'''
		strInput = strInput + '''<FACTORY NAME="" LINE ="" TESTER="'''
		strInput = strInput + self.stationName
		strInput = strInput + '''" FIXTURE="" SHIFT="" USER="'''
		strInput = strInput + self.userName
		strInput = strInput + '''" />'''
		strInput = strInput + '''<PRODUCT NAME="" REVISION="" FAMILY="" CUSTOMER="" />'''
		strInput = strInput + '''<REFS SEQ_REF="" FTS_REF="" LIM_REF="" CFG_REF="" CAL_REF="" INSTR_REF="" />'''
		strInput = strInput + '''<PANEL ID="'''
		strInput = strInput + UUTID
		strInput = strInput + '''" COMMENT="None" RUNMODE="Production" TIMESTAMP="" TESTTIME="0.000000" WAITTIME="0.000000" STATUS="'''
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
		strInput = strInput + '''"><GROUP NAME="'''
		strInput = strInput + strScriptName
		strInput = strInput + '''" STEPGROUP="'''
		strInput = strInput + strScriptName
		strInput = strInput + '''" GROUPINDEX="1" LOOPINDEX="0" TYPE="" RESOURCE="'''
		strInput = strInput + strScriptName
		strInput = strInput + '''" MODULETIME="0" TOTALTIME="0" TIMESTAMP="'''
		strInput = strInput + strTestStart
		strInput = strInput + '''" STATUS="'''
		strInput = strInput + strTestResult
		strInput = strInput + '''">'''

		for element in strTestArray.split(','):
			#print('element: {}'.format(element))
			#FORMAT: TEST NAME | RESULT | VALUE | LCL | UCL
			eleString = element.split("|")
			if self.debugMode == 1:  print('DEBUG ELESTRING: {}'.format(eleString))
			if len(eleString) > 1:
				# Result after Header
				strInput = strInput + '''<TEST NAME="'''
				strInput = strInput + eleString[0].strip()
				strInput = strInput + '''" DESCRIPTION="'''
				strInput = strInput + eleString[0].strip()
				strInput = strInput + '''" UNIT="" VALUE="'''
				strInput = strInput + eleString[2].strip()
				#strInput = strInput + strTestArray[1]
				strInput = strInput + '''" HILIM="'''
				strInput = strInput + eleString[4].strip()
				strInput = strInput + '''" LOLIM="'''
				strInput = strInput + eleString[3].strip()
				strInput = strInput + '''" STATUS="'''
				strInput = strInput + eleString[1].strip()
				strInput = strInput + '''" RULE="NONE" TARGET="" DATATYPE="String"/>'''

		# Footer
		strInput = strInput + '''</GROUP>'''
		strInput = strInput + '''</DUT></PANEL></BATCH>]]>'''
		strXMLResult = Raw(strInput)
		return strXMLResult
		


	
	
	