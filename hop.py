#! /usr/bin/env python3
import os
import re
import sys
from os import getcwd
from yaml import dump, safe_load
from yaml.error import YAMLError
from pathlib import Path

# List of colors for output
class Colors:
    RED       = '\033[0;31m'
    GREEN     = '\033[0;32m'
    PURPLE    = '\033[0;35m'
    LIGHTBLUE = '\033[0;96m'
    BGGRAY    = '\033[0;100m'
    GOLD      = '\033[0;33m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'

# Files and Directiries
FILE      = Path(__file__)
DIR       = FILE.parent
DATA_DIR  = DIR / "paths_cache"
HOPS_FILE = DATA_DIR / "saved_hops.yaml"

# returns:
#   -1      if invalid args
#    0      if successful
# otherwise, exists:
#   _path_  for shell script to cd to
def main():
    len_args = len(sys.argv)
    if (len_args > 1 and len_args < 4):
        list_hops = read_hops()
        str_action = sys.argv[1].lower()
        if (str_action == 'back'):
            if (len_args > 2):
                return handle_error('invalid_args')
            exit( hop_back( list_hops))
        if (str_action == 'help'):
            if (len_args > 2):
                return handle_error('invalid_args')
            return hop_help()
        if (str_action == 'ls'):
            if (len_args > 2):
                return handle_error('invalid_args')
            return hop_ls( list_hops)
        if (str_action == 'set'):
            if (len_args < 3):
                return handle_error('invalid_args')
            return hop_set( list_hops, hop_name=sys.argv[2])
        if (str_action == 'remove'):
            if (len_args < 3):
                handle_error('invalid_args')
            return hop_remove( list_hops, hop_name=sys.argv[2])
        if (str_action == 'reset'):
            if (len_args > 2):
                return handle_error('invalid_args')
            return hop_reset( list_hops)
        if (str_action == 'prune'):
            if (len_args > 2):
                return handle_error('invalid_args')
            return hop_prune( list_hops)
        if (str_action == 'rm' or str_action == 'delete'):
            return handle_error("use_remove_instead")
        # if str_action is not one of the above, it is considered a hop name
        if (len(sys.argv) > 2):
            return handle_error('invalid_args')
        exit(hop_to(str_action))
    else:
        return (handle_error('invalid_args'))


# reads hops from HOPS_FILE
def read_hops():
    with open( HOPS_FILE, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as exc:
            print(exc)
            return (0)


# writes hops to HOPS_FILE
def write_hops(list_hops):               
    with open( HOPS_FILE, 'w') as outfile:
        try:
            dump(list_hops, outfile, default_flow_style=False)
            return (0)
        except YAMLError as exc:
            print(exc)
            return (-1)
        
        
def hop_back(list_hops):
    # 1) check if no hop is active
    if (list_hops['history_prev_hop'] == None):
        handle_error('no_hop_active')
        return (0)
    # 2) if given hop_name's path is an existing directory
    if (not Path(list_hops['history_prev_hop']).is_dir()):
        handle_error('dir_does_not_exist')
        return (0)
    # if 1) and 2) are met, proceed to hop back at 'history_prev_hop'
    return (list_hops['history_prev_hop'])

 
def hop_to(hop_name):
    list_hops = read_hops()
    # 1) finds if hop exists
    if (hop_name not in list_hops):
        handle_error('hop_not_found')
        return (0)
    # 2) if already hopped 
    if (list_hops[hop_name] == getcwd()):
        handle_error('already_here')
        return (0)
    # 3) if given hop_name's path is an existing directory
    if (not Path(list_hops[hop_name]).is_dir()):
        handle_error('dir_does_not_exist')
        return (0)
        
    # if 1), 2), and 3) are met, return hop_name's path
    hop_path = list_hops[hop_name]
    # saves path of where we're hopping from
    list_hops['history_prev_hop'] = getcwd()
    write_hops(list_hops)
    return (hop_path)


def hop_ls(list_hops):
    rows, columns = os.popen('stty size', 'r').read().split()
    window_width = int(columns)
    separator_string_val = "-" * window_width
    print( separator_string_val)

    # if no hops exist, except 'history_prev_hop'
    if ( len(list_hops) == 1):
        print("\t [no 'hops' to give]")
    else:    
        # 1) get previous hop path
        previous_path = list_hops['history_prev_hop']
        # 2) print hops
        # delete placeholder 'history_prev_hop' so it dosent show up
        del list_hops['history_prev_hop']
        for key in list_hops:
            if (list_hops[key] == getcwd()):
                hop_name_color = Colors.GREEN+Colors.BOLD
                hop_path_color = Colors.GREEN+Colors.BOLD
                separator_color = Colors.GOLD+Colors.BOLD
            elif not hop_exists_at_path(list_hops[key]):
                hop_name_color = Colors.RED
                hop_path_color = Colors.RED
                separator_color = Colors.RED
            else:
                hop_name_color = Colors.LIGHTBLUE
                hop_path_color = Colors.ENDC
                separator_color = Colors.PURPLE

            if len(key) > 4:
                print(hop_name_color+f" {key} "+separator_color+" @ "+hop_path_color 
                    + format_path(key, list_hops[key], window_width)
                    + Colors.ENDC)  
            else:      
                 print(hop_name_color+f" {key} "+separator_color+"\t@ "+hop_path_color 
                    + format_path(key, list_hops[key], window_width)
                    + Colors.ENDC)                                      
                
        # 3) print last hopped from path
        if (previous_path != "-" and previous_path != None):
            print("\n"+Colors.BGGRAY+"Last Hopped From:"+Colors.ENDC+f"\n {previous_path}")
        else:
            print(Colors.RED+"\nNot hopped yet"+Colors.ENDC)

    print( separator_string_val)
    return (0)

def hop_exists_at_path(path):
    return (Path(path).is_dir())

def hop_set(list_hops, hop_name):
    # 1) checks if hop name is in restricted list
    list_restricted = ["set", "rm", "ls", "back", "help", 'history_prev_hop']
    if (hop_name in list_restricted):
        handle_error('hop_restricted_name')
        return (0)
    # 2) checks if name exists already
    if (hop_name in list_hops):
        handle_error('hop_already_exists')
        return (0)
    # if 1) and 2) are met, set hop
    print( f"Setting hop '{hop_name}' ...")
    # create new hop entry in list_hops like: "hop_name": "_current_path_"
    list_hops.update( {hop_name: getcwd()} )
    return (write_hops(list_hops))


def hop_remove(list_hops, hop_name):
    # checks if hop name exists and is not restricted
    if (hop_name in list_hops and hop_name != 'history_prev_hop'):
        print( f"Deleting hop '{hop_name}' ...")
        del list_hops[hop_name]
        return (write_hops(list_hops))
    else:
        handle_error('hop_not_found')
    return (0)
       

def hop_reset(list_hops):
    list_hops['history_prev_hop'] = "-"
    return write_hops(list_hops)

def hop_prune(list_hops):
    # mark hops with not directories at path
    to_be_removed_hops = []
    for key in list_hops:
        if (not Path(list_hops[key]).is_dir()):
            to_be_removed_hops.append(key)
    # if no hops to be removed
    if (len(to_be_removed_hops) == 0):
        handle_error('no_hops_to_remove')
        return (0)
    # use hop remove to remove hops
    for key in to_be_removed_hops:
        hop_remove( list_hops, hop_name=key)

def hop_help():
    print_help()


def format_path(hop_name, hop_path, window_width):
    margin = len(hop_name) + 4
    len_path = len(hop_path) + margin
    max_index = window_width - margin


    shortended = False
    if (len_path > max_index):
        cut = len_path - max_index
        hop_path = hop_path[cut:] # removees "./" from path
        shortended = True 
        
    if (shortended):
        index = hop_path.find("/")        
        hop_path = "(..)" + hop_path[index:]
    return hop_path            
            

def print_help():
    separator_string_val = "-" * 80
    print( separator_string_val)
    print("hop-command]\n - STRICT arg FORMAT\n - CASE INSENSITIVE\n"
        +"\n\thop _name_     - Hops to _name_ if exists."
        +"\n\thop "+Colors.GOLD+"ls"  +Colors.ENDC+"\t\t- Lists all saved hops."
        +"\n\thop "+Colors.GOLD+"set" +Colors.ENDC+" _name_\t- Saves a hop named _name_, pointing to current path."
        +"\n\thop "+Colors.GOLD+"remove " +Colors.ENDC+" _name_\t- removees hop."
        +"\n\thop "+Colors.GOLD+"back"+Colors.ENDC+"\t- Hops at 'last hopped from'."
        +"\n\thop "+Colors.GOLD+"reset"+Colors.ENDC+"\t- removees 'last hopped from' path."
        +"\n\thop "+Colors.GOLD+"prune"+Colors.ENDC+"\t- removees all hops with missing paths."
    )
    print( separator_string_val)


def handle_error(control_value):
    list_error = {
        "invalid_args":   "Invalid args.",                # 0
        "no_hop_active":  "You hopped yet.",              # 1
        "hop_not_found":  "No such hop exists.",          # 2
        "already_here":   "Already here.",                # 3
        "no_name_given":  "No name was given.",           # 4
        "hop_already_exists": "Hop already exists.",      # 5
        "hop_restricted_name": "Name given is restricted",# 6
        "dir_does_not_exist": "Directory does not exist.",# 7
        "no_hop_file": "Hop file does not exist",         # 8
        "use_remove_instead": "Use 'remove' instead.",    # 9
        "no_hops_to_remove": "No hops to remove.",        # 10
    }
    
    print("[hop] Error:", end=" ")
    print(list_error[control_value])
    if (control_value == "invalid_args"):
        print_help()
    if (control_value == "hop_restricted_name"):
        print(Colors.RED+"Restricted names: "+Colors.ENDC+"'set', 'rm', 'ls', 'back', 'help'")
    return (-1) # error was found since function was called

def __init__():
    if (not DATA_DIR.is_dir()):
        DATA_DIR.mkdir()
    if (not HOPS_FILE.is_file()):
        with open( HOPS_FILE, "w") as stream:
            stream.write("history_prev_hop: ")  

if __name__ == '__main__':
    __init__() # creates needed directories and files if not exist
    main()
#eOF file.py