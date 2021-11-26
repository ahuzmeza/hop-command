#! /Users/alinhuzmezan/.pyenv/shims/python3
import sys

from os import chdir, getcwd, getppid, kill, system
from signal import SIGHUP
from yaml import dump, safe_load
from yaml.error import YAMLError
from pathlib import Path

class bcolors:
    RED       = '\033[0;31m'
    GREEN     = '\033[0;32m'
    PURPLE    = '\033[0;35m'
    LIGHTBLUE = '\033[0;96m'
    BGGRAY    = '\033[0;100m'
    GOLD      = '\033[0;33m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'

FILE      = Path(__file__)
DIR       = FILE.parent
DATA_DIR  = DIR / "paths_cache"
HOPS_FILE = DATA_DIR / "saved_hops.yaml"
HISTORY_FILE = DATA_DIR / "saved_history.yaml"

def main():
    if (len(sys.argv) > 1 and len(sys.argv) < 4):
        list_hops = read_hops()
        str_action = sys.argv[1].lower()
        if (str_action == 'ls'):
            hop_ls( list_hops)
            return (1)
        if (str_action == 'set'):
            hop_set( list_hops)
            return (1)
        if (str_action == 'rm'):
            hop_rm( list_hops)
            return (1)
        if (str_action == 'back'):
            hop_back()
            return (-1)
        if (str_action == 'help'):
            print_help()
            return (1)
        if (str_action == 'reset'):
            hop_reset()
            return (1)
        
        # if arg1 is a valid, hop to hop path
        hop_to(str_action)       
    else:
        print_error('invalid_args')
        print_help()
        

# reads hops from HOPS_FILE
def read_hops():
    with open( HOPS_FILE, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as exc:
            print(exc)


# writes hops to HOPS_FILE
def write_hops(list_hops):
    with open( HOPS_FILE, 'w') as outfile:
        try:
            dump(list_hops, outfile, default_flow_style=False)
        except YAMLError as exc:
            print(exc)
        
        
# from a hops, hops back to where it was called   
def hop_back():
    list_hops = read_hops()
    # check if no hop is active
    if (list_hops['history_prev_hop'] == ""):
        print_error('no_hop_active')
    else:
        list_hops['history_prev_hop'] = ""
        write_hops(list_hops)
        
# instead will return path of history_prev_hop to shell function
        kill(getppid(), SIGHUP)
#################  

# tries to hop to specified hop
def hop_to(hop_name):
    list_hops = read_hops()
    
    # 1) finds if hop exists
    if (hop_name not in list_hops):
        print_error('hop_not_found')
        return
    # 2) if already hopped 
    if (hop_name == list_hops['history_prev_hop']):
        print_error('already_here')
        return
        
    # proceeds to hop if criteria 1) and 2) are met
    hop_path = list_hops[hop_name]
    # saves location of where we're hopping from
    list_hops['history_prev_hop'] = getcwd()
    write_hops(list_hops)
    
    print( f"Changing to '{hop_name}'\n@ {hop_path} ...")

# instead will return hop_path to shell function
        
    # change to hop path
    chdir(hop_path)
    # open new procces
    system('zsh')
    # --> prints after 'hop back'
    print( f"Hopped back at {list_hops['history_prev_hop']}")
###############################################################################


def hop_ls(list_hops):
    separator_string_val = "-" * 80
    print( separator_string_val)

    # if no hops exist
    if ( len(list_hops) == 1):
        print("\t [no 'hops' to give]")
        return
    
        # print active hop or not active status
       # if (list_hops['history_prev_hop'] != getcwd()):
       #     print( bcolors.GREEN + "Active: " 
       #           + bcolors.BOLD  + f"{list_hops['history_prev_hop']}" 
       #           + bcolors.ENDC
       #         )
        #active_hop_value = list_hops['history_prev_hop']
    
    # get previous hop path
    previous_path = list_hops['history_prev_hop']
    # delete placeholder 'history_prev_hop' so it dosent show up
    del list_hops['history_prev_hop']
    # print hops
    for key in list_hops:
        if (list_hops[key] == getcwd()):
            hop_name_color = bcolors.GREEN+bcolors.BOLD
            hop_path_color = bcolors.GREEN+bcolors.BOLD
            separator_color = bcolors.GOLD+bcolors.BOLD
        else:
            hop_name_color = bcolors.LIGHTBLUE
            hop_path_color = bcolors.ENDC
            separator_color = bcolors.PURPLE
        print(
              hop_name_color 
              + f" {key} " +
              separator_color
              + "\t@ " +
              hop_path_color 
              + f"{list_hops[key]} " + bcolors.ENDC
            )
    # print last hopped from path
    if (previous_path != ""):
        print("\n"+bcolors.BGGRAY+"Last Hopped From:"+bcolors.ENDC+f"\n {previous_path}")
    else:
        print(bcolors.RED+"\nNot hopped yet"+bcolors.ENDC)
    print( separator_string_val)
    

def hop_set(list_hops):
    if ( len(sys.argv) != 3):
        print_error(4)
        return
    
    hop_name = sys.argv[2]
    # check if name exists already
    if (hop_name in list_hops):
        print_error(5)
        return
       
    print( f"Setting hop '{hop_name}' ...")
    # create new hop entry in list_hops
    # hop_name: _current_path_
    list_hops.update( {hop_name: getcwd()} )
    write_hops(list_hops)
    

def hop_rm(list_hops):
    if ( len(sys.argv) != 3):
       print_error('no_name_given')
       return
    
    hop_name = sys.argv[2]
    if (hop_name in list_hops):
        print( f"Deleting hop '{hop_name}' ...")
        del list_hops[hop_name]
        write_hops(list_hops)
    else:
        print_error('hop_not_found')
       
###############################################################################
def hop_reset():
    list_hops = read_hops()
    list_hops['history_prev_hop'] = ""
    write_hops(list_hops)
###############################################################################

def print_help():
    separator_string_val = "-" * 80
    print( separator_string_val)
    print("hop-command]:"
        +"\n\thop "+bcolors.GOLD+"ls"  +bcolors.ENDC+"\t\t- lists all saved hops"
        +"\n\thop "+bcolors.GOLD+"set" +bcolors.ENDC+" _name_\t- saves a hop pointing to current path"
        +"\n\thop "+bcolors.GOLD+"rm " +bcolors.ENDC+" _name_\t- removes hop"
        +"\n\thop "+bcolors.GOLD+"back"+bcolors.ENDC+"\t- hops back where hopped from last"
        +"\n\thop _name_\t- hops to _name_ if exists"
    )
    print( separator_string_val)


def print_error(control_value):
    list_error = {
        "invalid_args":   "Invalid args.",        # 0
        "no_hop_active":  "No hop active.",       # 1
        "hop_not_found":  "No such hop exists.",  # 2
        "already_here":   "Already here.",        # 3
        "no_name_given":  "No name was given.",   # 4
        "already_exists": "Hop already exists."   # 5
    }
    
    print("[hop] Error:", end=" ")
    print(list_error[control_value])
    
    
if __name__ == '__main__':
    main()


# change list_hops to dictionary name,path
# ccreate shell alias witch switch case to call .p
# create hop_history of each location where hop was called
    # hop back will hop to previos_hop in hop_history

 
"""
2 args]
hop set      _name_  # uses python w/sane to set a hop named _name_
hop rm       _name_  # uses python w/sane to remove a hop named _name_

1 arg]
hop ls               # uses python w/sane to list all hops
hop _name_           # uses shell function to cd to _name_'s path
hop back             # uses shell function to cd to previous hop
"""

""" Restricted: 
    set 
    rm 
    ls
    back
    help
"""







