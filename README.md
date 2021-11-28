# hop-command
## Description
Describe

## Configure
 *1)* Clone this repository ___?where?___ you like.
 *2)* 'cd' into hop-command directory.
 *2)* 
 - a) Manually change python shabang in hop.py.
#### OR
 - b) run:$   sh setup.sh

#### This does:
- > Echos your python shabang into hop.py
- > Installs pyyaml with pip3
- > Makes hop.py exacutable by setting permission +x

**4)** Add following to shell config file. Eg: ~/.bashrc, ~/.zshrc etc

        # Hop command ###################################################
        export PATH=$PATH:_____?where?____/hop-command
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
        # ########################################################################
