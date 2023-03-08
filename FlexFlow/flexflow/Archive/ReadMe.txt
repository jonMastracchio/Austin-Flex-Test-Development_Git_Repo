*******************
CONFIG
*******************
name: FF_config.dat
Must be located in same directory as .exe
Asterisks behaves as a comment
|SERVER|FlexFlow web server address

*******************
GETUNITINFO
*******************

Command Ling Arguments

1) serialNumber
2) Station
3) User
4) Choice (1 or 0)
	- 1) output to console
	- 0) output to text file in GetUnitinfo directory

Example:
	- FFWebService.exe GetUnitInfo EDU01 FT1 admin 0
	- FFWebService.exe GetUnitInfo EDU01 FT1 admin 1

Requirements:
	- GetUnitInfo directory in path of executable
Example:
	- path\FFWebservice.exe
	- path\GetUnitInfo\


*******************
SaveResult
*******************

Command Ling Arguments

1) XMLPath
2) Station

Example:
	- FFWebService.exe SaveResult EDU01xml.xml FT1