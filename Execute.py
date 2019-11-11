import Query_target_device as QT
import Make_procedure as MP

#### Ver1.0 ####

########################################################
########################################################

if __name__ == "__main__":
	#POP = raw_input('Enter POP Code: ')
	#StartTime = raw_input('Enter PM Start time: ')
	#EndTime = raw_input('Enter PM End time: ')
	#ISP = raw_input('Enter ISP name: ')
	#Circuit = raw_input('Enter Target Circuit ID: ')
	
	POP = 'P37-ICN'
	ISP = 'KINX'
	Circuit = ['KINX-IX']
	Start_PM_Time = '2019-08-07 15:00'
	End_PM_Time = '2019-08-07 23:00'

	BGP_Info, Host_Info, Port_Info = QT.Find_Target_Device(POP,ISP,Circuit)
	
        MP.Make_pre_config(BGP_Info, Host_Info)
        MP.Make_post_config(BGP_Info, Host_Info)
	for i in Host_Info.keys():
		for j in Port_Info[i]:
			MP.Apply_task(Start_PM_Time, 'pre-check', i, Host_Info[i],j)
		MP.Apply_task(Start_PM_Time, 'pre-config', i, Host_Info[i],None)
		for j in Port_Info[i]:
			MP.Apply_task(End_PM_Time, 'post-check', i, Host_Info[i],j)
