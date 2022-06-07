from tkinter import *
from datetime import datetime, timedelta
import subprocess
import base64
import sys


##############  GLOBALS ############################################################################

subpro = subprocess.Popen(r'C:\Users\Florin.bosoi\Desktop\Germany\3 python test automation\3 server\wc3270\s3270.exe',
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE)
buffer = None
statusMsg = None
encoding = 'latin1'
MAXCC00 = 'MAXCC=0000'
MAXCC01 = 'MAXCC=0001'
MAXCC04 = 'MAXCC=0004'
CC00000 = '00000'
ABEND = 'ABENDED'
COMPLETED = 'FROM PDEU TO TDEB COMPLETED'
Sub = 'SUBMITTED'
End = 'ENDED'
JobSub = None
JobEnd = None
runs   = None
global ListCWA
ListCWA = []
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

       
def passCmd(cmd):
    cmd_bytes = cmd.encode('ascii')
    base64_bytes = base64.b64encode(cmd_bytes)
    base64_cmd = base64_bytes.decode('ascii')
    encoding = 'latin1'
    printLongLine()
    #This functions executes and displays the output of the command
    print('doCmd():', base64_cmd)
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
    global ResponseOk
    global JobOk
    global ResponseAB
    global TransferOk
    global Matched
    global JobSub
    global JobEnd
    global Skip
    TransferOk = None
    ResponseOk = None
    ResponseAB = None
    JobOk      = None
    Matched    = None
    Skip       = None 
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
    #When Jobs are submitted check for the response code
        if MAXCC00 in data or MAXCC04 in data or MAXCC01 in data:
            JobOk = ResponseOk = 'OK'
        else:
            JobOk = 'KO' 
        if ABEND in data:
            ResponseAB = 'Y'
        if COMPLETED in data:
            TransferOk = 'Y'
        if Sub in data:
           if len(val_user) < 7: 
              if data[29:32] == 'JOB':
                 JobSub = data[29:37]
              elif data[30:33] == 'JOB':
                 JobSub = data[30:38]   
              elif data[67:70] == 'JOB':
                 JobSub = data[67:75]   
           else:
              if data[30:33] == 'JOB':
                 JobSub = data[30:38]
              elif data[67:70] == 'JOB':
                 JobSub = data[67:75]
        if End in data and JobSub == data[16:24]:
            JobEnd  = data[16:24]
            Matched = 'Y'
        if CC00000 in data:
            Skip = 'Y'
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

def checkResp(cmd):
    i = 1
    while i < 7:
       cmd = "Wait(10,seconds)"
       doCmd(cmd)
    # Display Job finished successfully or Abended  
       if ResponseOk == 'OK' and Matched == 'Y':
          print('Response from script:  Submitted Job : ' + JobSub + ' and Ended Job : ' + JobEnd + ' matched.') 
          print("Response from script:  The previously Job has run successfully, your processing will continue normally.")
          break
       if Skip == 'Y':
          break 
       if ResponseAB == 'Y':
          sys.exit("The Job has not run successfully , please start the processing again from the begining, or check for the Job ABEND in JES.") 
    # Enter to refresh the screen if Job not finished
       cmd = 'Enter()'
       doCmd(cmd)
    # Display Job finished successfully  
       if ResponseOk == 'OK' and Matched == 'Y':
          print('Response from script:  Submitted Job : ' + JobSub + ' and Ended Job : ' + JobEnd + ' matched.') 
          print("Response from script:  The previously Job has run successfully, your processing will continue normally.")
          break
       if Skip == 'Y':
          break  
       if ResponseAB == 'Y':
          sys.exit("The Job has not run successfully , please start the processing again from the begining, or check for the Job ABEND in JES.") 
    # After 1 minute, if there is no ABEND but also no response from the Job, terminate the task    
       if i == 6 and (ResponseOk is None or JobOk == 'KO' or Matched is None):
          sys.exit("The Job has been timed out or has ended with MAXCC code greater than 04, please wait a while and start the processing again from the begining.") 
       i += 1

def waitTransfer(cmd):
    i = 1
    while i < 4:
          cmd = "Wait(10,seconds)"
          doCmd(cmd)
          if TransferOk == 'Y':
             print("Response from script:  Processing will continue.") 
             break
          cmd = 'Enter()'
          doCmd(cmd)
          if TransferOk == 'Y':
             print("Response from script:  Processing will continue.")
             break
          if i == 3 and TransferOk is None:
             sys.exit("Transfer of records has been timed out or has stopped abnormally, please restart the whole processing.") 
          i += 1

def runFdxdos():
   # create pop-up screen to ask for how many events FDXDOS will run 
    window = Tk()
    window.title('Establish the number of events to run')
 
   # specify size of window.
    window.geometry("920x250")
 
   # Create label
    l = Label(window, text = "Please select from below how many CWA based events do you wish to run and process.")
    l.config(font =("Courier", 14))
    l.pack()
   # Create button for text.
    for response in [1,2,3,4]:
       b = Button(window, text = response, command=lambda m=response: [respIs(m),window.destroy()])
       b.pack(pady = 10)
    
    window.mainloop()
    if runs is None:
       sys.exit("The number of events for the run hasn't been chosed, please run again and make your choice.")
    else:
       print("Your chosen event run number for FDXDOS aging is : ", runs)

def respIs(response):
    global runs
    runs = response

def retrieveTimebefore():
    global t
    global d
    curDT = datetime.today() - timedelta(hours=1, minutes=0)
    t = curDT.strftime('%H:%M:%S')
    d = curDT.strftime('%Y-%m-%d')
    
def retrieveTimeafter():
    global t1
    global d1
    curDT = datetime.today() - timedelta(hours=1, minutes=0)
    t1 = curDT.strftime('%H:%M:%S')
    d1 = curDT.strftime('%Y-%m-%d')

def runBaseline():
    i = 1
    while runs >= i:
          #Recover the timestamp for French time to have it for UNDODB2 data
          retrieveTimebefore()
          
          # Set the CWA date used for Job run
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTDATE)\' ")'
          doCmd(cmd)
          
          val_CWA = input("Please insert CWA date in format DD.MM.SSYY of the event to run and press Enter to continue : ")
          cmd = 'String("\'")' + 'String("' + val_CWA + '")' + 'String("\'")'
          doCmd(cmd)

          # create list with CWA dates used for COMPARISON of files later
          ListCWA.append(val_CWA)

          cmd = 'Enter()'
          doCmd(cmd)

          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)
          
          # Submit FDXDOS Job
          cmd = 'String("TSO SUBMIT (\'TDEBQSM.LIB.ART.JCL(BASELINE)\')")'
          doCmd(cmd)
    
          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)
          
          # Take the timestamp after FDXDOS runs
          retrieveTimeafter()

          # Set the timestamp used for DB2#BASE run START
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTT)\' ")' + 'String("\'")' + 'String("S")' + 'String("' + d + '")' + 'String("-")' + 'String("' + t + '")' + 'String("\'")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          # Set the timestamp used for DB2#BASE run END
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTT)\' ")' + 'String("\'")' + 'String("E")' + 'String("' + d1 + '")' + 'String("-")' + 'String("' + t1 + '")' + 'String("\'")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          # Submit DB2#BASE Job
          cmd = 'String("TSO SUBMIT (\'TDEBQSM.LIB.ART.JCL(DB2#BASE)\')")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)


          i += 1

def runRelease():
    # reimport the foyers and vendors
    importRelease()
    i = 1
    while runs >= i:
          #Recover the timestamp for French time to have it for UNDODB2 data
          retrieveTimebefore()
          
          # Set the CWA date used for Job run
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTDATE)\' ")'
          doCmd(cmd)
          
          val_CWA = input("Please insert CWA date in format DD.MM.SSYY for the event run and press Enter to continue : ")
          cmd = 'String("' + val_CWA + '")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)
          
          # Submit FDXDOS Job
          cmd = 'String("TSO SUBMIT (\'TDEBQSM.LIB.ART.JCL(RELEASE#)\')")'
          doCmd(cmd)
    
          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)
          
          # Take the timestamp after FDXDOS runs
          retrieveTimeafter()

          # Set the timestamp used for DB2#REL run START
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTT)\' ")' + 'String("\'")' +  'String("S")' +  'String("' + d + '")' + 'String("-")' + 'String("' + t + '")' + 'String("\'")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          # Set the timestamp used for DB2#BASE run END
          cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTT)\' ")' + 'String("\'")' +  'String("E")' + 'String("' + d1 + '")' + 'String("-")' + 'String("' + t1 + '")' + 'String("\'")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          # Submit DB2#REL Job
          cmd = 'String("TSO SUBMIT (\'TDEBQSM.LIB.ART.JCL(DB2#RELS)\')")'
          doCmd(cmd)

          cmd = 'Enter()'
          doCmd(cmd)

          #Wait for the response of the job RC = 00
          checkResp(cmd)

          cmd = 'Enter()'
          doCmd(cmd)


          i += 1

def importRelease():
    # Submit the PRODFOY job for the foyer file
    cmd = 'String("TSO PRODFOY FILE")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Insert the PROD environment for Germany
    cmd = 'String("PDEU")'
    doCmd(cmd)

    # Insert the Baseline Test environment for Germany
    cmd = 'String("TDEC")'
    doCmd(cmd)

    # Insert the T option for transfer foyer
    cmd = 'String("T")'
    doCmd(cmd)

    # Move cursor to position to insert file name
    cmd = 'MoveCursor(14,12)'
    doCmd(cmd)

    # Insert the file name for the transfer of foyer to be submitted
    cmd = 'String("TPRGPPL.TESTCASE.MCD#2021.FOYER")'
    doCmd(cmd)

    # Submit the transfer Job for foyers
    cmd = 'Enter()'
    doCmd(cmd)

    #Wait for the response of the job RC = 00
    checkResp(cmd)
    waitTransfer(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Submit the PRODFOY job for the foyer file
    cmd = 'String("TSO PRODVDR FILE")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Insert the PROD environment for Germany
    cmd = 'String("PDEU")'
    doCmd(cmd)

    # Insert the Baseline Test environment for Germany
    cmd = 'String("TDEC")'
    doCmd(cmd)

    # Insert the T option for transfer foyer
    cmd = 'String("T")'
    doCmd(cmd)

    # Move cursor to position to insert file name
    cmd = 'MoveCursor(13,12)'
    doCmd(cmd)

    # Insert the file name for the transfer of foyer to be submitted
    cmd = 'String("TPRGPPL.TESTCASE.MCD#2021.VDR")'
    doCmd(cmd)

    # Submit the transfer Job for foyers
    cmd = 'Enter()'
    doCmd(cmd)

    #Wait for the response of the job RC = 00
    checkResp(cmd)
    waitTransfer(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

def compareFiles():
    for i in range(len(ListCWA)):
        # Set the CWA date used for Job run
        cmd = 'String("TSO CALL \'TDEAAPP.CREDIT.LNKBA.TDEB(ARTDATE)\' ")' + 'String("' + ListCWA[i] + '")'
        doCmd(cmd)

        cmd = 'Enter()'
        doCmd(cmd)

        checkResp(cmd)

        cmd = 'Enter()'
        doCmd(cmd)

        cmd = 'String("TSO SUBMIT \'TDEBQSM.LIB.ART.JCL(COMP#DB2)\' ")'
        doCmd(cmd)

        checkResp(cmd)

        cmd = 'Enter()'
        doCmd(cmd)
        
def printLongLine():
    print('------------------------------------------------------------------------------')
 

def main():
    #Main
    print("Hello, world!")

    runFdxdos()

    print("Opening s3270.exe")

    print("Sending the command ")

    #s3270 command: Connect(172.21.2.135)
    cmd ="Connect(172.21.2.135)"
    doCmd(cmd)

    #s3270 cmd: Wait the screen to show something
    cmd = "Wait(3270mode)"
    doCmd(cmd)

    cmd = 'String("TPX")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    #Connect with user and password by showing the password encoded
    global val_user
    val_user = input("Please insert USER and press Enter to continue...")
    cmd = 'String("' + val_user + '")'
    doCmd(cmd)

    cmd = 'Tab()'
    doCmd(cmd)

    val_pass = input("Please insert PASSWORD and press Enter to continue...")
    cmd = 'String("' + val_pass + '")'
    passCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    #Enter to PDF menu in mainframe
    cmd = 'Tab()'
    doCmd(cmd)

    cmd = 'Tab()'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    cmd = 'String("1")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)
    
    cmd = 'String("TSO SUBMIT (\'TDEBQSM.LIB.ART.JCL(TEST#GEN)\')")'
    doCmd(cmd)
    
    cmd = 'Enter()'
    doCmd(cmd)

    #Wait for the response of the job RC = 00
    checkResp(cmd)

    cmd = 'Enter()'
    doCmd(cmd)
  
    # Submit the PRODFOY job for the foyer file
    cmd = 'String("TSO PRODFOY FILE")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Insert the PROD environment for Germany
    cmd = 'String("PDEU")'
    doCmd(cmd)

    # Insert the Baseline Test environment for Germany
    cmd = 'String("TDEB")'
    doCmd(cmd)

    # Insert the T option for transfer foyer
    cmd = 'String("T")'
    doCmd(cmd)

    # Move cursor to position to insert file name
    cmd = 'MoveCursor(14,12)'
    doCmd(cmd)

    # Insert the file name for the transfer of foyer to be submitted
    cmd = 'String("TPRGPPL.TESTCASE.MCD#2021.FOYER")'
    doCmd(cmd)

    # Submit the transfer Job for foyers
    cmd = 'Enter()'
    doCmd(cmd)

    #Wait for the response of the job RC = 00
    checkResp(cmd)
    waitTransfer(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Submit the PRODFOY job for the foyer file
    cmd = 'String("TSO PRODVDR FILE")'
    doCmd(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Insert the PROD environment for Germany
    cmd = 'String("PDEU")'
    doCmd(cmd)

    # Insert the Baseline Test environment for Germany
    cmd = 'String("TDEB")'
    doCmd(cmd)

    # Insert the T option for transfer foyer
    cmd = 'String("T")'
    doCmd(cmd)

    # Move cursor to position to insert file name
    cmd = 'MoveCursor(13,12)'
    doCmd(cmd)

    # Insert the file name for the transfer of foyer to be submitted
    cmd = 'String("TPRGPPL.TESTCASE.MCD#2021.VDR")'
    doCmd(cmd)

    # Submit the transfer Job for foyers
    cmd = 'Enter()'
    doCmd(cmd)

    #Wait for the response of the job RC = 00
    checkResp(cmd)
    waitTransfer(cmd)

    cmd = 'Enter()'
    doCmd(cmd)

    # Run Baseline and Release aging with events
    runBaseline()

    runRelease()

    compareFiles()
    
    #End script   
    quit()
#########################################################################################################
if __name__ == '__main__':
    main()









#s3270 command: 


