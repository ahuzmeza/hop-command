# hop-command
## Description:
A terminal command that lets you save directory paths as 'hops',
so you can easily cd to your favourite paths.

## Install & Configure:
#### 1) Clone this repository ___?where?___ you like.
#### 2) Add hop.py shabang.
#### 3) Install 'pyyaml'.

### How?
   a) Manually

   b) run:$ **`sh setup.sh`**
   - This does:

> Echos your python shabang into hop.py

> Installs pyyaml with pip3

#### 4) Add following to shell config file. Eg: ~/.bashrc, ~/.zshrc etc
   
   **And replace** -----?where?----- (see step 1.)

        # Hop command --------------------------------------------------
        export PATH=$PATH:-----?where?-----/hop-command
        # hop.py returns:
        #       1) output to be printed  => print output
        #       2) a path to a directory => cd to that path
        alias hop='hop-sh'
        hop-sh ()
        {
                HOP=$(hop.py $@ 2>&1)
        
                if [ -d "$HOP" ]; then
                        cd "${HOP}"
                        echo "Arrived @ $PWD"
                else
                        echo "$HOP"
                fi
        }
        # --------------------------------------------------------------
