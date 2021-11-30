# hop-command
## Description:
A terminal command that lets you save directory paths as 'hops',
so you can easily cd to your favourite paths.

## Install & Configure:
### Easy way:  :fish:
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


### Manually:
##### 1) Clone this repository ----?where?---- you like.
##### *) Change hop.py permission if needed.
##### 2) :exclamation:Have 'pyyaml' installed.
##### 3) Create shell function:
##### a) Place the following in shell config file.  Eg: ~/.bashrc, ~/.bash_profile, ~/.zshrc, etc.

> The following is the content of 'hop_shell_source'

export PATH=$PATH:----?where?----/hop-command
\# hop.py returns:
\#       1) output to be printed  => print output
\#       2) a path to a directory => cd to that path
hop ()
{
        HOP=$(hop.py $@ 2>&1)
        
        if [ -d "$HOP" ]; then
                cd "${HOP}"
                echo "Arrived @ $PWD"
        else
                echo "$HOP"
        fi
}
\# --------------------------------------------------------------

### Or
#### b) Change ----?where---- in 'hop_shell_source' and source it in shell config file.
\# Hop command --------------------------------------------------
source ----?where?----/hop_shell_source
\# --------------------------------------------------------------



