
from jinja2 import Environment, FileSystemLoader
import yaml
import pprint
from datetime import date

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

