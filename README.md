# Vendor PM Automation
This script support automatically traffic shift before vendor maintenance, 
and rollback traffic after maintenance time with verification status.
Usually Local vendor proceed maintenance in the midnight,
It is too hard that engineer standby that time and take action manually.
So, script will control traffic with pre-defined solution without human

[Purpose]
 - Traffic control automatically with crontab job : prevent to waste human resources

[Function]
 1) Gather BGP policy(route-map) from target router that is connected target maintenance circuit
 2) Define pre/post-configuration with gathered BGP policy
 3) Register crontab job with maintenance time and configuration running script
 4) Crontab run scheduled script and traffic will be shifted to other circuit
 5) After maintenance time, crontab run verifying script and check current status at target circuit
 6) In the working time, engineer check current status and rollback traffic
    
[Manual]
 - how to run script and input option 

        Execute.py                      # Run execution file
            Enter POP Code:             # Enter DC name(Country, location)
            Enter PM Start time:        # Enter Maintenance start time (Timezone : GMT)
            Enter PM End time:          # Enter Maintenance end time (Timezone : GMT)
            Enter ISP name:             # Enter Circuit vendor name
            Enter Target Circuit ID:    # Enter maintenance target circuit ID
 - Check crontab scheduler
        
            crontab -l
 - Check pre/post-configuration, current status : Configuration directory is located at same directory with execution file
            
            cat ./pre_task_information/"Year""Month""Day".txt       # port status before maintenance
            cat ./pre_config/"Year""Month""Day".txt                 # pre-configuration
            cat ./post_config/"Year""Month""Day".txt                # post-configuration
 - Check port status after maintenance
 
            cat ./post_task_information/"Year""Month""Day".txt      # port status after maintenance

            
            
[Requirement]
 - Python Version higher than 3.0
 - Running_Script repository
 - Tracking_Network_event repository
 
[Supported Vendor]
 - Juniper EX/QFX/MX series with JUNOS
 - Cisco Catalyst series with IOS
 - Cisco Nexus series with NXOS
 - Arista with EOS
 - Ubiquoss
 - Huawei
 - Foundry & Broucade
 - Dell
 - Ruijie
 
[Note]
 - Will be added automatic traffic rollback function : Compare port status before and after, then rollback by script
 - Now, only support Juniper router. Will be add more vendor option when new model is installed
