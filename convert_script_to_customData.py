#!/usr/bin/env python
# The main idea is to convert any script which use some of Azure elements (i.e "parameters" and "variables") 
# and fit to customData attribute in Azure template so we can inject that script into a provisioned Azure VM. 
# Note that there is a need to supply azure_template.json file (sample of Azure template file) and take customData from there after the script is finish

#usage: python convert_script_to_customData.py <script to convert> <azure_template.json file> 

from collections import OrderedDict
import os
import re
import json
import sys

customData = []

#argv[0] is the command name
if len(sys.argv) != 3:
   print "usage: python convert_script_to_customData.py <script to convert> <azure template.json file>"
   sys.exit(0) 

with open(sys.argv[1]) as f:
    for line in f:
        m = re.match(r'(.*?)(parameters\([^\)]*\))(.*$)', line)
        if m:
            customData += ['\'' + m.group(1) + '\'',
                           m.group(2),
                           '\'' + m.group(3) + '\'',
                           '\'\n\'']
        else:
            m = re.match(r'(.*?)(variables\([^\)]*\))(.*$)', line)
            if m:
                customData += ['\'' + m.group(1) + '\'',
                           m.group(2),
                           '\'' + m.group(3) + '\'',
                           '\'\n\'']
            else:
                customData += ['\'' + line + '\'']

with open(sys.argv[2]) as f:
    templ = json.load(f, object_pairs_hook=OrderedDict)
    templ['variables']['customData'] = '[concat(' + ', '.join(
        customData) + ')]'

os.rename(sys.argv[2], 'azuredeploy.json.old')

with open(sys.argv[2], 'w') as f:
    f.write(json.dumps(templ, indent=2).replace(' \n', '\n') + '\n')
