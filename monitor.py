import time,socket
import json as js

file_to_monitor = ('./file.json')

# Initially load the config file
oldfile = open(file_to_monitor,'rb')
old = js.load(oldfile)
oldfile.close()

# Function to send change log to notification service over socket
def invoke_notification_svc(changed_info):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostbyname("localhost")
  s.connect((host, 8800))
  s.sendall(changed_info)

# Function to detect changes made to Wireless APs file
def identify_changes(old,new,reset_flag):
  if old is None or new is None:
    return 'Empty'
  actual_data = old['access_points']
  changed_data = new['access_points']
  changed_info = ''
  for element in actual_data:
    if element['ssid'] in [ entry['ssid'] for entry in changed_data ]:
      for field in changed_data:
        if element['ssid']==field['ssid']:
          if element['snr']!=field['snr']:
            changed_info += element['ssid']+"'s SNR value changed from "+str(element['snr'])+" to "+str(field['snr'])+"\n"
          if element['channel']!=field['channel']:
            changed_info += element['ssid']+"'s Channel value changed from "+str(element['channel'])+" to "+str(field['channel'])+"\n"
    else:
      changed_info += element['ssid']+" is removed from the list\n"
  for field in changed_data:
    if field['ssid'] not in [pat['ssid'] for pat in actual_data ]:
      changed_info += field['ssid']+" is newly added to the list with SNR "+str(field['snr'])+" and channel "+str(field['channel'])+"\n"
  if changed_info == '':
    print 'No Changes detected'
    pass
  else:
    #print(changed_info)
    print 'Changes informed to notification service'
    invoke_notification_svc(changed_info)
    reset_flag = 1
    return reset_flag


if __name__ == '__main__':
  while True:
    with open(file_to_monitor,'rb') as changed:
      new = js.load(changed)
    reset_flag = 0
    reset_flag = identify_changes(old,new,reset_flag)
    # Consider updated file as the new reference file
    if reset_flag == 1:
      oldfile = open(file_to_monitor,'rb')
      old = js.load(oldfile)
      oldfile.close()
    time.sleep(2)
