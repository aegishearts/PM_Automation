import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from Running_Script import Run_Command as RUN
import Make_procedure as MP

#### Ver1.0 ####

########################################################
########################################################

if __name__ == "__main__":
	task = sys.argv[1]
	config_file = sys.argv[2]
	Hostname = sys.argv[3]
	Vendor = sys.argv[4]
	if task == 'pre-check' or task == 'post-check':
		Value = sys.argv[5]
	if task == 'pre-check':
                MP.Make_check_status(Hostname, Vendor, Value, config_file)
	elif task == 'pre-config':
		RUN.Apply_Config(Hostname, Vendor, config_file)
	elif task == 'post-check':
                MP.Make_check_status(Hostname, Vendor, Value, config_file)
		#### Need to add function :: compare pre-task result. if no issue, run post-config
		#### check crontab last job => Get time => +30minutes => Create crontab job for post-config
		#### reset crontab job after post-config 'crontab -r'
