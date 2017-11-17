#!/usr/bin/env python
###########################
import fileinput

#make sure each parameters is in new line - only parameters and vaiables attributes are supported
#if ithere is a need to support other attributes there is a need to change converting script as well

server_dict = {}
server_dict["LINUX_CMD"] =     "parameters('linuxCommand')"

#file which will hold the generated configuration
output_file=open("/mnt/cf/injected_command.txt", "a+")

def run_linux_command():
    if "LINUX_CMD" in server_dict:
        if len(server_dict["LINUX_CMD"]) > 1:
            output_file.write("command is" + server_dict["LINUX_CMD"]+"\n")


run_linux_command()
