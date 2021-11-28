# installs pyyaml with pip
pip3 install pyyaml

# creates shell_hop_source file
echo "\n# Hop command --------------------------------------------------
export PATH=\$PATH:$PWD
# hop.py returns:
#       1) output to be printed  => print output
#       2) a path to a directory => cd to that path
alias hop='hop-sh'
hop-sh ()
{
        HOP=\$(hop.py \$@ 2>&1)
        
        if [ -d "\$HOP" ]; then
                cd "\${HOP}"
                echo "Arrived @ $PWD"
        else
                echo "\$HOP"
        fi
}
# --------------------------------------------------------------\n" > hop_shell_source

# source file to ~/.bashrc
echo "\n# Hop command --------------------------------------------------" >> ~/.bashrc 
echo "source $PWD/hop_shell_source" >> ~/.bashrc 
echo "# --------------------------------------------------------------\n" >> ~/.bashrc

source ~/.bashrc
