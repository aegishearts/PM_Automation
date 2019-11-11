import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from Running_Script import Query_DB as DB
from Running_Script import Run_Command as RUN
from Running_Script import Check_config as CFG

#### Ver1.0 ####

########################################################

########################################################

def Find_Target_Device(POP, ISP, Circuit_List):
	SW_List = DB.Search_All_Device_by_POP(POP)
	BGP_DIC = {}
	Host_DIC = {}
	Port_DIC = {}
	for i in SW_List:
		if 'bb' in i:
		        Vendor,Code = DB.Search_Host_NIDB(i)
			RST = CFG.Find_Port_by_Description(i,Vendor,Circuit_List)
			if not RST == None:
				DIC = CFG.Find_BGP_Group_Name_for_IX(i,Vendor,RST)
				DenyPL = CFG.Find_BGP_DenyAll_Policy(i, Vendor)
				for j in DIC.keys():
					DIC[j][0].remove(DenyPL)
					DIC[j][1].remove(DenyPL)
					DIC[j].append(DenyPL)
					BGP_DIC[i] = DIC
					Host_DIC[i] = Vendor
					Port_DIC[i] = RST.keys()
	return BGP_DIC, Host_DIC, Port_DIC
