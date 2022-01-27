import json
import sys
import requests
import urllib3
import subprocess as sp
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
headers = urllib3.make_headers(basic_auth='skocharlakota:<PASSWORD>')
url     = 'https://vm-mgr01.infra.dc.srekoc.net/rest/com/vmware/cis/session'
payload = {}
#headers = {'Accept': 'application/json'}
res = requests.post(url, data=payload, headers=headers, verify=False)
print (res.text)