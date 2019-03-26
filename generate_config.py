
from jinja2 import Environment, FileSystemLoader
import yaml
import pprint
from datetime import date
import napalm

#Read YAML File into Python Dict
yaml_file = open('config-device1')
config = yaml.load(yaml_file)

#pprint.pprint(config)

#Load Jinja2 template
env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.j2')

#Render template using the config ,print and save the output
for device in config:
    print("===============================")
    rendered_config = template.render(device)
#Save Output to File with todays date and Hostname as filename
    saveoutput = open(str(date.today()) + '-' + device['hostname'] + '.txt', 'w')
    saveoutput.write(rendered_config)
    saveoutput.write('\n')
    saveoutput.close()
    print(rendered_config)
    print("===============================")


#NAPALM Driver Cred to Access Cisco IOS Device
devicelist = ['10.3.255.102']


#Loop trough each IP Address and validate the current config against the template
for ip_address in devicelist:
    print ("Connecting to " + str(ip_address))
    print("===============================")
    driver = napalm.get_network_driver('ios')
    ios = driver(ip_address, 'python', 'cisco')
    ios.open()
    ios.load_replace_candidate(config= rendered_config)
    diffs = ios.compare_config()
    if len(diffs) > 0:
        print('config has changed')
        print("===============================")
        print("===========Changes:============")
        print(diffs)
        print("===============================")
        ios.commit_config()
    else:
        print('Nothing has changed')
        ios.discard_config()