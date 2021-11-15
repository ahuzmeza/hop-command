#!/bin/bash
from os import getcwd, getcwdb
import sys

from yaml import dump, safe_load
from yaml.error import YAMLError

#   Add $: hop __name__
#   if found - cd __name
#   else     - error NotFound
#

def main():
    
    if (len(sys.argv) > 1 and len(sys.argv) < 4):
        list_hops = read_hops()
        str_action = sys.argv[1].lower()
        if (str_action == 'set'):
            set_hop( list_hops)
        if (str_action == 'ls'):
            show_hops( list_hops)
        if (str_action == 'del'):
            delete_hop( list_hops)            
    else:
        print("Error:", end=" ")
        print("Invalid args.")


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
    with open("saved_paths.yaml", "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as exc:
            print(exc)


def write_hops(list_hops):
    with open("saved_paths.yaml", 'w') as outfile:
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
