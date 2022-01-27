import sys, os
from docker_cmds import getPythonLayers, buildPythonImages

#add them to a overall dict
cmds = {
        'getPythonLayers' : getPythonLayers,
        'buildPythonImages' : buildPythonImages,
       }

try:
    cmd = sys.argv[1] 
    params = sys.argv[2:] # return everything after the first param in a list
    if(params):
        cmds[cmd]['fn'](params)
    else:
        cmds[cmd]['fn']()
except IndexError as e:
    # print(f'Error: {e}')
    print("You need to pass a cmd!")
    print("Commands: ")
    for c, value in cmds.items():
        print(f'    • {c} - {value["help"]}')
    
