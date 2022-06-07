import textwrap
from ftplib import FTP
import webbrowser
import os

sess = FTP("172.21.2.135", "STOICA", "CETT1010")

dir = "C:\\Users\\andrei.stoica\\Desktop\\py scripts\\ftp part"
hostfile = "TDEBQSM.JANUS.COMP#DB2.ENVS"
writeFile = "ftpDownload.txt"

lines = []
sess.retrlines("RETR 'TDEBQSM.JANUS.COMP#DB2.ENVS'", lines.append)
pcfile = open("%s/%s"% (dir,writeFile), 'w')

for line in lines:
    pcfile.write(line+"\n")



pcfile.close()
sess.quit()



contents = open("%s/%s"% (dir,writeFile), "r")

with open("output.html", "w") as e:
    for lines in contents.readlines():
#        e.write("<pre>" + lines + "</pre> <br>")
        e.write("<pre>" + lines + "</pre>")

with open("output.html", "r", encoding='utf-8') as f:
    text= f.read()
    
filename = "output.html"
webbrowser.open('file://' + os.path.realpath(filename))
