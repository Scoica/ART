from tkinter import *
import subprocess


##############  GLOBALS ############################################################################
#subprocess.call('C:\\Users\\andrei.stoica\\Desktop\\temp\\3 server\\wc3270\\s3270.exe')

subpro = subprocess.Popen('C:\\Users\\andrei.stoica\\Desktop\\temp\\3 server\\wc3270\\s3270.exe',
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)
buffer = None
statusMsg = None
encoding = 'latin1'
############## /GLOBALS ############################################################################

def doCmd(cmd):
    encoding = 'latin1'
    printLongLine()
    #This functions executes and dispplays the output of the command
    print('doCmd():', cmd)
    cmd = cmd.encode(encoding) + b'\n'
    subpro.stdin.write(cmd)
    subpro.stdin.flush()
    #just show the first 5 lines
    for repeat in range(0, 90):
        data = subpro.stdout.readline().decode(encoding).rstrip('\n').rstrip('\r')
        print("Response from script: ", data)
        if data == 'ok':
            break
    waitCmd()
    printCmd()

def printCmd():
    printLongLine()
    #The same thing as doCmd but only for printing
    cmd ="PrintText(string)"
    print('doCmd():', cmd)
    cmd = cmd.encode(encoding) + b'\n'
    subpro.stdin.write(cmd)
    subpro.stdin.flush()
    #just show the first 5 lines
    for repeat in range(0, 90):
        data = subpro.stdout.readline().decode(encoding).rstrip('\n').rstrip('\r')
        print("Response from script: ", data)
        if data == 'ok':
            break

def waitCmd():
    printLongLine()
    #The same thing as doCmd but only for printing
    cmd = "Wait(1,seconds)"
    print('doCmd():', cmd)
    cmd = cmd.encode(encoding) + b'\n'
    subpro.stdin.write(cmd)
    subpro.stdin.flush()
    #just show the first 5 lines
    for repeat in range(0, 90):
        data = subpro.stdout.readline().decode(encoding).rstrip('\n').rstrip('\r')
        print("Response from script: ", data)
        if data == 'ok':
            break

def printLongLine():
    print('------------------------------------------------------------------------------')

def main():
    #Main
    print("Hello, world!")

    print("Opening s3270.exe")

    print("Sending the command ")

    #s3270 command: Connect(172.21.2.135)
    cmd ="Connect(172.21.2.135)"
    doCmd(cmd)

    #s3270 cmd: Wait the screen to show something
    cmd = "Wait(3270mode)"
    doCmd(cmd)

    #Return the screen contents as text.
    #cmd ="PrintText(string)"
    #doCmd(cmd)

    #Return the screen contents as HTML.
    #cmd ="PrintText(string,html)"
    #doCmd(cmd)

    cmd = 'String("TPX")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    input("Press Enter to continue...")
    
#########################################################################################################
if __name__ == '__main__':
    main()









#s3270 command: 








#check return
'''
 data = subpro.stdout.readline().decode.rstrip('\n').rstrip('\r')
        if not data.startswith('data:'):
            statusMsg = data
        else:
            buffer = data[6:]
            data = subpro.stdout.readline().decode.rstrip('\n').rstrip('\r')
            if not data.startswith('data:'):
                statusMsg = data
            else:
                buffer += '\n' + data[6:]
                go = True
                while go:
                    data = self.subpro.stdout.readline().decode(self.encoding).rstrip('\n').rstrip('\r')
                    if not data.startswith('data:'):
                        go = False
                        statusMsg = data
                    else:
                        self.buffer += '\n' + data[6:]

        returnMsg = self.subpro.stdout.readline().decode(self.encoding).rstrip('\n').rstrip('\r')
        self.statusMsg = StatusMessage(statusMsg)
        logger.debug("Buffer data    => [{}]".format(self.buffer))
        logger.debug("Status message => [{}]".format(statusMsg))
        logger.debug("Return message => [{}]".format(returnMsg))
        if returnMsg == 'ok':
            return True
        return False
'''























#C:\Users\andrei.stoica\Desktop\temp\3 server\wc3270-4.0ga14-noinstall-32\s3270.exe
#C:\Users\andrei.stoica\Desktop\temp\3 server\wc3270

#subprocess.call('C:\\Users\\andrei.stoica\\Desktop\\temp\\3 server\\wc3270\\s3270.exe')


#
