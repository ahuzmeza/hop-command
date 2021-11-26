#! /Users/alinhuzmezan/.pyenv/shims/python3
import sys

from os import chdir, getcwd, getgid, getppid, kill, system
from signal import SIGHUP
from yaml import dump, safe_load
from yaml.error import YAMLError
from pathlib import Path

class bcolors:
    RED    = '\033[0;31m'
    GREEN  = '\033[0;32m'
    PURPLE = '\033[0;35m'
    GOLD   = '\033[0;33m'
    GRAYBG = '\033[0;96m'
    ENDC   = '\033[0m'
    BOLD   = '\033[1m'

FILE      = Path(__file__)
DIR       = FILE.parent
DATA_DIR  = DIR / "paths_cache"
HOPS_FILE = DATA_DIR / "saved_hops.yaml"
HISTORY_FILE = DATA_DIR / "saved_history.yaml"


def main():
    print(f"hop.py PPID>{getppid()}")

    if (len(sys.argv) > 1 and len(sys.argv) < 4):
        list_hops = read_hops()
        str_action = sys.argv[1].lower()
        if (str_action == 'set'):
            set_hop( list_hops)
            return
        if (str_action == 'ls'):
            show_hops( list_hops)
            return
        if (str_action == 'rm'):
            delete_hop( list_hops)
            return
        if (str_action == 'back'):
            hop_back()
            return
        if (str_action == 'reset'):
            hop_reset()
            return
        # if arg1 is a valid, hop to hop path
        tryhop(str_action)       
    else:
        print("Error:", end=" ")
        print("Invalid args.")

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
        dump(list_hops, outfile, default_flow_style=False)

        
# from a hops, hops back to where it was called   
def hop_back():
    list_hops = read_hops()
    # check if no hop is active
    if (list_hops['hop_active'] == '-'):
        print("Error: No hop active.")
        return
    # else
    list_hops['hop_active'] = "-"
    write_hops(list_hops)
    kill(getppid(), SIGHUP)
    

# tries to hop to specified hop
def tryhop(hop_name):
    list_hops = read_hops()
    
    # 1) finds if hop exists
    if (hop_name not in list_hops):
        print( f"Error: Hop '{hop_name}' does not exist.")
        return
    # 2) if already hopped 
    if (hop_name == list_hops['hop_active']):
        print("Already hopped.\tTry '" 
            + bcolors.GOLD + "hop back"
            + bcolors.ENDC + "'\nTo get to where you hopped from."
            )
        return
        
    # proceeds to hop if criteria 1) and 2) are met
    try:
        hop_path = list_hops[hop_name]
        # marks hop_active as true
        list_hops['hop_active'] = hop_name
        write_hops(list_hops)
        
        hopped_from = getcwd()
        print( f"Changing to {hop_name} @ {hop_path}...")
        # change to hop path
        chdir(hop_path)
        # open new procces
        system('zsh')

        # --> prints after 'hop back'
        print( f"Hopped back at {hopped_from}")
    except Exception as e:
        print(e)
        print( f"Error: Hop {hop_name} not found.")


def show_hops(list_hops):
    separator_string_val = "-" * 80
    print( separator_string_val)

    # if no hops exist
    if ( len(list_hops) == 1):
        print("\t [no 'hops' to give]")
    else:
        # print active hop or not active status
        if (list_hops['hop_active'] == '-'):
             print( bcolors.RED + "Inactive" + bcolors.ENDC)
        else:
            print( 
                  bcolors.GREEN + "Active: " 
                  +  bcolors.BOLD  + f"{list_hops['hop_active']}" 
                  + bcolors.ENDC
                )

        active_hop_value = list_hops['hop_active']
        del list_hops['hop_active']
        # print hops
        for key in list_hops:
            if (list_hops[key] == active_hop_value):
                hop_name_color = bcolors.GREEN
                hop_path_color = bcolors.GREEN
            else:
                hop_name_color = bcolors.GRAYBG
                hop_path_color = bcolors.ENDC
            print(
                  hop_name_color 
                  + f" {key} " +
                  bcolors.PURPLE 
                  + "\t@ " +
                  hop_path_color 
                  + f"{list_hops[key]} "
                )
    print( separator_string_val)
    

def set_hop(list_hops):
    if ( len(sys.argv) != 3):
        print("Error:", end=" ")
        print("No name was given.")
        return
    
    hop_name = sys.argv[2]
    # check if name exists already
    # return - if duplicate
    if (hop_name in list_hops):
        print( f"Error: Hop '{hop_name}' already exists.")
        return
       
    print( f"Setting hop {hop_name}...")
    # create new hop entry in list_hops
    # hop_name: _current_path_
    list_hops.update( {hop_name: getcwd()} )
    write_hops(list_hops)
    

def delete_hop(list_hops):
    if ( len(sys.argv) != 3):
       print("Error:", end=" ")
       print("No name was given.")
       return
    
    hop_name = sys.argv[2]
    if (hop_name in list_hops):
        print( f"Deleting hop {hop_name}...")
        del list_hops[hop_name]
        write_hops(list_hops)
    else:
        print("Error:", end=" ")
        print( f"Hop '{hop_name}' dosen't exists.")


# resets 'hop_active' to 0
def hop_reset():
    list_hops = read_hops()
    list_hops['hop_active'] = "-"
    write_hops(list_hops)


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
hop rm       history # uses python w/sane to delete all paths in history
hop ls       _name_  # uses python w/sane to list all hops

1 arg]
hop history          # uses python w/sane to list history

hop _name_           # uses shell function to cd to _name_'s path
hop back             # uses shell function to cd to previous hop
"""
""" Restricted: 
    set 
    rm 
    history 
    ls
    back 
"""







