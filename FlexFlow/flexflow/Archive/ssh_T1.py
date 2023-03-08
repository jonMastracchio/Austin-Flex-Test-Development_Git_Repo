import threading, paramiko, time, warnings, platform, os, load_ff_, flexflow
# os:           Check OS version of executable. Will change directory format
# load_ssh_:    Load ssh paramters
# load_ff_:     Load FlexFlow paramters
# parse_ssh_:   Parse ssh report
# flexflow:     Access to FlexFlow API's

warnings.filterwarnings(action='ignore',module='.*paramiko.*')

print(platform.system())
strPlatform = platform.system()
# Windows
# Linux
strdata=''
fulldata=''

########################################################################################################################
class ssh:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address))
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)

        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def close_connection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def open_shell(self):
        self.shell = self.client.invoke_shell()

    def send_shell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def process(self):
        global strdata, fulldata
        while True:
            # Print data when available
            if self.shell is not None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = strdata + str(alldata)
                fulldata = fulldata + str(alldata)
                strdata = self.print_lines(strdata) # print all received data except last line

    def print_lines(self, data):
        last_line = data
        if '\n' in data:
            lines = data.splitlines()
            #for i in range(0, len(lines)-1):
                #print(lines[i])
            last_line = lines[len(lines) - 1]
            if data.endswith('\n'):
                #print(last_line)
                last_line = ''
        return last_line

if __name__ == "__main__":
    ####################################################################################################################
    # Load from Parameter files.
    #
    strTester = load_ff_.load_ff_parameters('strTester')
    strStationName = load_ff_.load_ff_parameters('strStationName')
    strUser = load_ff_.load_ff_parameters('strUser')

    # sshUsername = load_ssh_.load_ssh_parameters('sshUsername')
    # sshPassword = load_ssh_.load_ssh_parameters('sshPassword')
    # sshServer = load_ssh_.load_ssh_parameters('sshServer')

    ####################################################################################################################
    # FlexFlow Station Call
    #
    flexflow.wsGetUnitInfo(strTester, 'VC20050024', strStationName, strUser)
    #flexflow.wsGetUnitInfo(strTester,'DailyFT1SN',strStationName,strUser)
    #f = open("test_PASS.xml", "r")
    #if f.mode == 'r':
    #    contents = f.read()
    #flexflow.wsSaveResult(strTester, contents, strStationName)
    # import flexflow; flexflow.wsSaveResult(strTester, 'DailyHipotSN_.xml', strStationName)

    ####################################################################################################################
    # SSH into Remote Tester
    #
    try:
        connection = ssh(sshServer, sshUsername, sshPassword)
        print('Connection Successful')
    except:
        print('Connection Failed')
        quit()

    connection.open_shell()
    time.sleep(2)
    connection.send_shell('sudo -i')
    connection.send_shell(sshPassword)
    time.sleep(2)
    connection.send_shell('')
    connection.send_shell('')
    connection.send_shell('')
    connection.send_shell('cd /home/aurzeus/Documents/Hot_Swap_PCIe')
    time.sleep(2)
    connection.send_shell('')
    connection.send_shell('')
    connection.send_shell('')
    connection.send_shell('ls')
    time.sleep(2)
    connection.send_shell('')
    connection.send_shell('')
    connection.send_shell('')

    print('===================================================='
          '====================================================')

    connection.close_connection()

    ####################################################################################################################
    # Parse SSH report and determine test status
    #
    contents = parse_ssh_.parser(fulldata)
    print(contents)