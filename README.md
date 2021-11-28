# hop-command
## Description:
A terminal command that lets you save directory paths as 'hops',
so you can easily cd to your favourite paths.

## Install & Configure:
### Using **`sh setup.sh`**. :fish:
##### 1) Clone and cd to directory.
##### 2) Use: **`sh setup.sh`**.
##### *) Change hop.py permission using **`chmod +x hop.py`** if needed.
##### *) Restart your terminal if needed. :heavy_check_mark:
- This does:

> Installs pyyaml with pip3

> Creates 'shell_hop_source' file

> Appends 'ource shell_hop_source' to ~/.bashrc

> Tries to set permission to hop.py

> Tries to restart terminal by sourcing ~/.nashrc


### Manually:
##### 1) Clone this repository ----?where?---- you like.
##### *) Change hop.py #!shabang if needed.
##### *) Change hop.py permission if needed.
##### 2) Make sure you have 'pyyaml' installed.
##### 3) Add following to shell config file. Eg: ~/.bashrc, ~/.bash_profile, ~/.zshrc, etc.
##### And edit ----?where?----.
        
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





