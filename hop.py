#! /Users/alinhuzmezan/.pyenv/shims/python3
import sys

from os import chdir, getcwd, getppid, kill, system
from signal import SIGHUP
from yaml import dump, safe_load
from yaml.error import YAMLError
from pathlib import Path

class bcolors:
    RED    = '\033[0;31m'
    GREEN  = '\033[0;32m'
    PURPLE = '\033[0;35m'
    ENDC   = '\033[0m'
    BOLD   = '\033[1m'

FILE = Path(__file__)
DIR = FILE.parent
HOPS_DIR = DIR / "saved_hops"
HOPS_FILE = HOPS_DIR / "saved_paths.yaml"

def main():
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
        # if arg1 is a valid hop name sys cd to hop path
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
    
    for hop in list_hops['hops']:
        if (hop['name'] == 'hop_active'):
            if (hop['path'] != "-"):
                hop['path'] = "-"
                write_hops(list_hops)
                kill(getppid(), SIGHUP)
                return
    # if no hop_active to hop back
    print("No hop active")


# tries to hop to specified hop
def tryhop(hop_name):
    list_hops = read_hops()
    
    # 1) finds if hop exists
    found = False
    for hop in list_hops['hops']:
        if (hop['name'] == hop_name):
            #print( f"Trying hop {hop_name} at {hop['path']}")
            hop_path = hop['path']
            found = True
            break
    
    # 2) determines if already in a hop
    already_hopped = False
    for hop in list_hops['hops']:
        if (hop['name'] == 'hop_active'):
            if (hop['path'] != "-"):
                print("already hopped")
                already_hopped = True
    
    # proceeds to hop if criteria 1) and 2) are met
    if (found and not already_hopped):
        try:
            # marks hop_active as true
            for hop in list_hops['hops']:
                if (hop['name'] == 'hop_active'):
                    hop['path'] = hop_name
                    break
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
    if ( len(list_hops['hops']) == 0):
        print("\t [no 'hops' to give]")
    else:
        # print active hop or not active status
        if (list_hops['hops'][0]['path'] == '-'):
             print( bcolors.RED + "Inactive" + bcolors.ENDC)
        else:
            print( 
                  bcolors.GREEN + "Active: " 
                  +  bcolors.BOLD  + f"{list_hops['hops'][0]['path']}" 
                  + bcolors.ENDC
                )
        
        
        # prubt hops
        for entry in list_hops['hops'][1:] :
            if (entry['name'] == list_hops['hops'][0]['path']):
                print( 
                  bcolors.GREEN + f"{entry['name']}" 
                  + bcolors.PURPLE + "\t@ " 
                  + bcolors.ENDC
                  + bcolors.GREEN + f"{entry['path']} "
                ) 
            else:
                print( 
                      f"{entry['name']}" 
                      + bcolors.PURPLE + "\t@ " 
                      + bcolors.ENDC
                      + f"{entry['path']} "
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
    for hop in list_hops['hops']:
        if (hop['name'] == hop_name):
            print("Error:", end=" ")
            print( f"Hop '{hop_name}' already exists.")
            return
        
    hop_path = getcwd()
    
    new_hop = {'name': hop_name, 'path': hop_path}
    list_hops['hops'].append(new_hop)
    print(new_hop)
    print( f"Setting hop {hop_name}...")
    write_hops(list_hops)
    

def delete_hop(list_hops):
    if ( len(sys.argv) != 3):
       print("Error:", end=" ")
       print("No name was given.")
       return
    
    hop_name = sys.argv[2]
    foundBy_hop_name = False
    for hop in list_hops['hops']:
        if (hop['name'] == hop_name):
            list_hops['hops'].remove(hop)
            foundBy_hop_name = True
    
    if (foundBy_hop_name):
        print( f"Deleting hop {hop_name}...")
        write_hops(list_hops)
    else:
        print("Error:", end=" ")
        print( f"Hop '{hop_name}' dosen't exists.")

# resets 'hop_active' to 0
def hop_reset():
    list_hops = read_hops()
    for hop in list_hops['hops']:
        if (hop['name'] == 'hop_active'):
            hop['path'] = "-"
            write_hops(list_hops)
            return


if __name__ == '__main__':
    main()















