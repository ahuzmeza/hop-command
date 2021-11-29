# hop-command
## Description:
A filesystem mobility tool for the shell.

`hop set _name_` saves a named 'hop' poinring to current dir.

`hop _name_` cd's you to its path.

`hop ls` lists all available hops.

> see `hop help` for details.

## Install & Configure:
### Easy way: :snail:
##### 1) Clone and cd to directory.
##### 2) Use: $**`sh setup.sh`**.
##### *) Change hop.py permission using **`chmod +x hop.py`** if needed.
##### :wavy_dash:) Restart terminal :heavy_check_mark:
- This does:

> Installs pyyaml with pip3

> Creates 'shell_hop_source' file

> Appends "source 'shell_hop_source'" in ~/.bashrc

> Tries to set permission to hop.py

> Tries to restart terminal by sourcing ~/.bashrc


### Manually: :hammer:
##### 1) Clone this repository ----?where?---- you like.
##### *) Change hop.py permission if needed.
##### 2) :exclamation:Have 'pyyaml' installed.
##### 3) Place the following in shell config file.  Eg: ~/.bashrc, ~/.bash_profile, ~/.zshrc, etc.
    # Hop command --------------------------------------------------

    source ----?where?----/hop_shell_source

    # --------------------------------------------------------------



