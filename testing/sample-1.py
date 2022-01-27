'''
import subprocess
output = subprocess.getoutput("ssh verdad01 stdbuf -oL central-push")
print(output)
'''

import subprocess

cmd = "ssh verdad01 central-push"

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
stdout = []
while True:
    line = p.stdout.readline()
    if not isinstance(line, (str)):
        line = line.decode('utf-8')
        line = line.strip()
    stdout.append(line)
    print (line)
    if (line == '' and p.poll() != None):
        break

output, errors = p.communicate()
print ("Errors >> " + errors)
