import platform, os
strPlatform = platform.system()

def load_ff_parameters(element):
    stringTempArray = []
    stringElement = ''
    if strPlatform.strip() == 'Windows':
        path = os.getcwd() + '\FLEXFLOW\Flexflow_Parameters.txt'
    if strPlatform.strip() == 'Linux':
        path = os.getcwd() + '/FLEXFLOW/Flexflow_Parameters.txt'

    # Open a file
    with open(path , 'r') as f:
        lines = f.readlines() # readlines creates a list of the lines
    if element == 'strTester':
        stringTempArray = lines[0].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strStationName':
        stringTempArray = lines[1].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strUser':
        stringTempArray = lines[2].split('|')
        stringElement = stringTempArray[1].strip()

    return stringElement
	
def load_ff_SnP_parameters(element):
    stringTempArray = []
    stringElement = ''
    if strPlatform.strip() == 'Windows':
        path = os.getcwd() + '\FLEXFLOW\Flexflow_SNP_Parameters.txt'
    if strPlatform.strip() == 'Linux':
        path = os.getcwd() + '/FLEXFLOW/Flexflow_SNP_Parameters.txt'

    # Open a file
    with open(path , 'r') as f:
        lines = f.readlines() # readlines creates a list of the lines
    if element == 'strTester':
        stringTempArray = lines[0].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strStationName':
        stringTempArray = lines[1].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strUser':
        stringTempArray = lines[2].split('|')
        stringElement = stringTempArray[1].strip()

    return stringElement
	
def load_ff_RmA_parameters(element):
    stringTempArray = []
    stringElement = ''
    if strPlatform.strip() == 'Windows':
        path = os.getcwd() + '\FLEXFLOW\Flexflow_RMA_Parameters.txt'
    if strPlatform.strip() == 'Linux':
        path = os.getcwd() + '/FLEXFLOW/Flexflow_RMA_Parameters.txt'

    # Open a file
    with open(path , 'r') as f:
        lines = f.readlines() # readlines creates a list of the lines
    if element == 'strTester':
        stringTempArray = lines[0].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strStationName':
        stringTempArray = lines[1].split('|')
        stringElement = stringTempArray[1].strip()
    if element == 'strUser':
        stringTempArray = lines[2].split('|')
        stringElement = stringTempArray[1].strip()

    return stringElement
	
if __name__ == "__main__":
	print(load_ff_parameters('strTester'))
	print(load_ff_parameters('strStationName'))
	print(load_ff_parameters('strUser'))