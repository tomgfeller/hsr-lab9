from jinja2 import Environment, FileSystemLoader
import yaml
import pprint
from datetime import date
from datetime import datetime
import napalm
from time import sleep
import git
from git import repo

# Read YAML File into Python Dict
yaml_file = open('config-device1')
config = yaml.load(yaml_file)

# pprint.pprint(config)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.j2')

# The While Loop runs all the code every 60 Seconds --> Compliance Check
while True:

    # Render template using the config ,print and save the output
    for device in config:
        print("==============================================================")
        rendered_config = template.render(device)
        # Save Output to File with todays date and Hostname as filename
        saveoutput = open(str(date.today()) + '-' + device['hostname'] + '.txt', 'w')
        saveoutput.write(rendered_config)
        saveoutput.write('\n')
        saveoutput.close()
        print(rendered_config)
        print("==============================================================")

        #Pull connection_address attribute from the yaml config-device1 file
        connection_address = device['connection_address']

        #Connection to the devices
        print(str(datetime.now()) + " Connecting to " + str(connection_address))
        print("==============================================================")
        driver = napalm.get_network_driver('ios')
        ios = driver(connection_address, 'python', 'cisco')
        ios.open()
        # Replacing the config if the difference is > than 0 characters
        ios.load_replace_candidate(config=rendered_config)
        diffs = ios.compare_config()
        if len(diffs) > 0:
            print('config has changed')
            print("==============================================================")
            print("===========================Changes:===========================")
            print(diffs)
            print("==============================================================")
            ios.commit_config()
        else:
            print('Nothing has changed')
            ios.discard_config()
    sleep(60)