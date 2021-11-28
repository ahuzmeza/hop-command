# hop-command
## Description:
A terminal command that lets you save directory paths as 'hops',
so you can easily cd to your favourite paths.

## Install & Configure:
### Using **`sh setup.sh`**. :fish:
##### 1) clone and cd to directory.
##### 2) run:$ **`sh setup.sh`**.
##### 3) restart your terminal. :heavy_check_mark:
- This does:

> Installs pyyaml with pip3

> Creates 'shell_hop_source' file

> Appends 'ource shell_hop_source' to ~/.bashrc


### Manually:
##### 1) Clone this repository ----?where?---- you like.
##### 2) Make sure you have 'pyyaml' installed.
##### 3) Add following to shell config file. Eg: ~/.bashrc, ~/.bash_profile, ~/.zshrc, etc
##### And edit ----?where?---- (see step 1.)
        
        # Hop command --------------------------------------------------"
        export PATH=$PATH:----?where?----
        alias hop='hop-sh'
        hop-sh ()
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





