# hop-command
  # Description
Describe

  # Configure
1) clone this repository ___?where?___ you like
2) cd into hop-command directory
2) manually change python shabang
OR
run:$   sh setup.sh

This does:
- echos your python shabang into hop.py
- installs pyyaml with pip3
- makes hop.py exacutable by setting permission +x
4) add following to shell config file. Eg: ~/.bashrc, ~/.zshrc etc

        # # Hop command ###################################################
        # export PATH=$PATH:_____?where?____/hop-command
        # # hop.py returns:
        # #   1) output to be printed  => print output
        # #   2) a path to a directory => cd to that path
        # alias hop='hop-sh'
        # hop-sh ()
        # {
        #         HOP=$(hop.py $@ 2>&1)
        # 
        #         if [ -d "$HOP" ]; then
        #                 cd "${HOP}"
        #                 echo "Arrived @ $PWD"
        #         else
        #                 echo "$HOP"
        #         fi
        # }
        # ########################################################################
