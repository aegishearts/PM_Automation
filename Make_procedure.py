import os,sys, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from datetime import datetime
from Tracking_Network_event import Interface_Status_Checker as INTS

#### Ver1.0 ####

########################################################
today = datetime.today().strftime('%Y%m%d')
Pre_config_txt = '/XXXXXX/PM_Automation/pre_config/'+today+'.txt'
Post_config_txt = '/XXXXXX/PM_Automation/post_config/'+today+'.txt'
Pre_task_info = '/XXXXXX/PM_Automation/pre_task_information/'+today
Post_task_info = '/XXXXXX/PM_Automation/post_task_information/'+today
########################################################

def JUNOS_Make_pre_config(BGP_DIC):
	f = open(Pre_config_txt,'w')
	for i in BGP_DIC.keys():
		Import_List = BGP_DIC[i][0]
		Export_List = BGP_DIC[i][1]
		First_IMP = Import_List[0]
		First_EXP = Export_List[0]
		DenyAll = BGP_DIC[i][2]
		f.write('set protocols bgp group '+i+' import '+DenyAll+'\n')
		f.write('insert protocols bgp group '+i+' import '+DenyAll+' before '+First_IMP+'\n')
		f.write('set protocols bgp group '+i+' export '+DenyAll+'\n')
		f.write('insert protocols bgp group '+i+' export '+DenyAll+' before '+First_EXP+'\n')
	f.close()

def JUNOS_Make_post_config(BGP_DIC):
	f = open(Post_config_txt,'w')
	for i in BGP_DIC.keys():
		Import_List = BGP_DIC[i][0]
		Export_List = BGP_DIC[i][1]
		Last_IMP = Import_List[-1]
		Last_EXP = Export_List[-1]
		DenyAll = BGP_DIC[i][2]
		f.write('insert protocols bgp group '+i+' import '+DenyAll+' after '+Last_IMP+'\n')
		f.write('insert protocols bgp group '+i+' export '+DenyAll+' after '+Last_EXP+'\n')
	f.close()

def Make_pre_config(BGP_DIC, Host_Info):
	for i in Host_Info.keys():
		Vendor = Host_Info[i]
		if Vendor == 'juniper':
			JUNOS_Make_pre_config(BGP_DIC[i])

def Make_post_config(BGP_DIC, Host_Info):
	for i in Host_Info.keys():
		Vendor = Host_Info[i]
		if Vendor == 'juniper':
			JUNOS_Make_post_config(BGP_DIC[i])

def Make_check_status(Host, Vendor, Port, File):
	f = open(File,'a')
	if 'ae' in Port:
		return None, None
	else: 
		OS = INTS.Query_Interface_Optic(Host,Vendor,Port)
		PR = INTS.Query_Interface_Information(Host,Vendor,Port)
	f.write(Host+'\n')
	f.write(json.dumps(OS))
	f.write('\n')
	f.write(json.dumps(PR))
	f.write('\n')
	f.close()

def Apply_task(Time, Step, Host, Vendor, Value):
	M = Time.split()[0].split('-')[1]
	D = Time.split()[0].split('-')[2]
	h = Time.split()[1].split(':')[0]
	m = Time.split()[1].split(':')[1]
	if Step == 'pre-check':
		config_file = Pre_task_info
		CMD = m+' '+h+' '+D+' '+M+' * /usr/local/bin/python /XXXXXX/PM_Automation/Do_task.py '+Step+' '+config_file+' '+Host+' '+Vendor+' '+Value
	elif Step == 'pre-config':
		config_file = Pre_config_txt
		CMD = m+' '+h+' '+D+' '+M+' * /usr/local/bin/python /XXXXXX/PM_Automation/Do_task.py '+Step+' '+config_file+' '+Host+' '+Vendor
	elif Step == 'post-check':
		config_file = Post_task_info
		CMD = m+' '+h+' '+D+' '+M+' * /usr/local/bin/python /XXXXXX/PM_Automation/Do_task.py '+Step+' '+config_file+' '+Host+' '+Vendor+' '+Value
	os.system('(crontab -l 2>\/dev\/null; echo \"'+CMD+'\") | crontab -')
