# hop-command
## Description:
A terminal command that lets you save directory paths as 'hops',
so you can easily cd to your favourite paths.

## Install & Configure:
### Easy way:  :fish:
##### 1) Clone and cd to directory.
##### 2) Use: $ **`sh setup.sh`**.
##### *) Change hop.py permission using **`chmod +x hop.py`** if needed.
##### +) Restart terminal :heavy_check_mark:
- This does:

> Installs pyyaml with pip3

> Creates 'shell_hop_source' file

> Appends "source 'shell_hop_source'" in ~/.bashrc

> Tries to set permission to hop.py

> Tries to restart terminal by sourcing ~/.bashrc


### Manually:
##### 1) Clone this repository ----?where?---- you like.
##### *) Change hop.py #!shabang if needed.
##### *) Change hop.py permission if needed.
##### 2) Make sure you have 'pyyaml' installed.
##### 3) Add following to shell config file. Eg: ~/.bashrc, ~/.bash_profile, ~/.zshrc, etc.
###### or source 'hop_shell_source' file in shell config.
###### And edit ----?where?----.
        
__in: /hop-command/hop_shell_source:

        # Hop command --------------------------------------------------"
        export PATH=$PATH:----?where?----
        hop()
        {
                HOP=\$(hop.py $@ 2>&1)

                if [ -d "$HOP" ]; then
                        cd "${HOP}"
                        echo "Arrived @ $PWD"
                else
                        echo "$HOP"
                fi
        }
        # --------------------------------------------------------------"





