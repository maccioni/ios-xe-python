import os
import sys
from cli import cli
import time
import difflib
import requests,json,time,datetime

#
# Info to be provided: Tropo Toke, Spark room ID and Spark Token
#
# Add Tropo Token
tropoapi='https://api.tropo.com/1.0/sessions?action=create&token=<tropo-token>'
# Add Spark Room ID
roomId=''
# Add Spark Token
auth=''


def compare_configs(cfg1,cfg2):

  d = difflib.context_diff(cfg1, cfg2)

  diffstr = ""
  previousline=''
  for line in d:
    templine= "\n" + line
    if line.find('Current configuration') == -1:
      if line.find('Last configuration change') == -1:
        if (line.find("+++")==-1) and (line.find("---")==-1):
          if (line.find("-!")==-1) and (line.find('+!')==-1):
            if (line.find("length")==-1):
              if line.startswith('+'):
                diffstr = diffstr + previousline + "\n" + line
              elif line.startswith('-'):
                diffstr = diffstr + previousline + "\n" + line
            else:
              previousline=templine

  return diffstr

if __name__ == '__main__':

  script=sys.argv[0]

#If a second arguments is provided, enable debug
  if len(sys.argv) > 1 :  debug=True
  else :                  debug=False

  if debug: print  script + ' starting '

##OLD
  f = open('/bootflash/old_cfg')
  old_cfg = f.readlines()
  f.close

##RENEW
  output = cli('show run')
  f = open('/bootflash/new_cfg',"w")
  f.write(output)
  f.close
  f = open('/bootflash/new_cfg',"r")
  new_cfg = f.readlines()
  f.close

##DIFF (This snippet is Not really needed, only if you want to store the code differences in the switch)
  diff =  compare_configs(old_cfg,new_cfg)
  f = open("/bootflash/diff","w")
  f.write(diff)
  f.close

##WRITEOLD
  f = open('/bootflash/old_cfg',"w")
  f.write(output)
  f.close

  d = datetime.datetime.now() - datetime.timedelta(hours=8)
  hostname=cli('show run | inc hostname')
  hostname=hostname.replace("\n","")
  hostname=hostname.replace(" ","")
  hostname=hostname.replace("hostname","")

  diff=diff.replace('\n','\\n')
  diff=diff.replace('\\n+ !','')
  diff=diff.replace('\\n- !','')
  diff=diff.replace('-','Removed: ')
  diff=diff.replace('+','Added: ')

  headers2 = {'Authorization': 'Bearer '+auth, 'Content-Type': 'application/json; charset=utf-8' }

  if debug: print  script + ' posting on spark room'

  #Spark Message
  data =unicode('{"markdown":"## \\ud83d\\udd34 Configuration Change Alert! \\n Hello! There has been a configuration change on Switch: **' + hostname + '** as of '+d.strftime('%A, %B %d, at %-I:%M %p.') + '\\n These are the changes: \\n'+ str(diff)+'\\n **This is not a drill!**","roomId": "'+roomId+'"}"','utf-8')
  req2 = requests.post('https://api.ciscospark.com/v1/messages',data=data,headers=headers2)

  if debug: print  script + ' connecting to tropo APIs'

  #Tropo Voice Call Message
  diff=diff.replace('\\n',' , ')
  data=json.dumps({ "msg": 'alert, alert, Hello! There has been a configuration change on switch, ' + hostname + ', as of, ' \
  + d.strftime('%A, %B %d, at, %-I %M %p,') + ', these are the changes,   ' + diff + ', this is not a drill, to dismiss, say dismiss, or hang up. To escalate, say escalate.'})

  headers = {'Content-Type': 'application/json'}
  req3 = requests.post(tropoapi,
                      data=data,headers=headers)
