from flexflow import *

ff=flexflow('09 - AUTO FCT TEST [430]','aurjomas','http://aurnt090/ZeusFFTesterWS/FFTesterWS.asmx?WSDL')
ff.set_debugMode(1)
ff.print_inputs()

unitResult = ff.wsGetUnitInfo('VC20310013')
print('GetUnitInfo UnitResult: {}'.format(unitResult[0]))
print('GetUnitInfo UnitInfo: {}'.format(unitResult[1]))

testResult = ff.createXMLTestResult('VC20310013', 'Passed', 'Test1|Passed|5|0|10,Test2|Passed|5|0|10,Test3|Passed|5|0|10','ThisIsAtest.py')
print('XMLRESULT: {}'.format(testResult))

print('SaveResult Status: {}'.format(ff.wsSaveResult(testResult)))