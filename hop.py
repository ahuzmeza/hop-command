#! /Users/alinhuzmezan/.pyenv/shims/python3
from os import PathLike, _exit, chdir, getcwd, getcwdb, getpgid, getppid, kill, system
import sys
import pathlib
import signal

from yaml import dump, safe_load, serialize
from yaml.error import YAMLError

#   Add $: hop __name__
#   if found - cd __name
#   else     - error NotFound
#

FILE = pathlib.Path(__file__)
DIR = FILE.parent
HOPS_DIR = DIR / "saved_hops"
HOPS_FILE = HOPS_DIR / "saved_paths.yaml"

def main():
    if (len(sys.argv) > 1 and len(sys.argv) < 4):
        list_hops = read_hops()
        str_action = sys.argv[1].lower()
        if (str_action == 'set'):
            set_hop( list_hops)
        if (str_action == 'ls'):
            show_hops( list_hops)
        if (str_action == 'rm'):
            delete_hop( list_hops)
        if (str_action == 'back'):
            hop_back()
        # if arg1 is a valid hop name sys cd to hop path
        tryhop(str_action)       
    else:
        print("Error:", end=" ")
        print("Invalid args.")

def hop_back():
    list_hops = read_hops()
    
    for hop in list_hops['hops']:
        if (hop['name'] == 'hop_active'):
            if (hop['path'] == 1):
                hop['path'] = 0
                write_hops(list_hops)
                kill(getppid(), signal.SIGHUP)
                return
    # if no hop_active to hop back
    print("no hop active to hop back")

def tryhop(hop_name):
    list_hops = read_hops()
    
    found = False
    for hop in list_hops['hops']:
        if (hop['name'] == hop_name):
            #print( f"Trying hop {hop_name} at {hop['path']}")
            hop_path = hop['path']
            found = True
            break
    
    already_hopped = False
    for hop in list_hops['hops']:
        if (hop['name'] == 'hop_active'):
            if (hop['path'] == 1):
                print("already hopped")
                already_hopped = True
    
    if (found and not already_hopped):
        try:
            for hop in list_hops['hops']:
                if (hop['name'] == 'hop_active'):
                    hop['path'] = 1
                    break
            write_hops(list_hops)
            
            print( f"Changing to {hop_name} @ {hop_path}...")

            # change to hop path
            chdir(hop_path)
            # open new procces
            system('zsh')
        
            print( "All set!")
        except Exception as e:
            print(e)
            print( f"Error: Hop {hop_name} file not found.")


def show_hops(list_hops):
    separator_string_val = "-" * 80
    print( separator_string_val)

    # if no hops exist
    if ( len(list_hops['hops']) == 0):
        print("\t [no 'hops' to give]")
    else:
        for entry in list_hops['hops']:
            print( f" {entry['name']} @ {entry['path']} ")
    print( separator_string_val)


def read_hops():
    with open( HOPS_FILE, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as exc:
            print(exc)


def write_hops(list_hops):
    with open( HOPS_FILE, 'w') as outfile:
        dump(list_hops, outfile, default_flow_style=False)


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

 


if __name__ == '__main__':
    main()















