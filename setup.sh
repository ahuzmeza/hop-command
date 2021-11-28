# installs pyyaml with pip
echo "-> Installing pyyaml..."
pip3 install pyyaml
echo "-> Finished."


# creates shell_hop_source file
echo -n "-> Creating shell_hop_source file... "
echo "# Hop command --------------------------------------------------
export PATH=\$PATH:$PWD
# hop.py returns:
#       1) output to be printed  => print output
#       2) a path to a directory => cd to that path
hop ()
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
echo "<- Finished"

# source file to ~/.bashrc
echo -n "-> Appending source to ~/.bashrc... "

echo "# Hop command --------------------------------------------------
source $PWD/hop_shell_source" >> ~/.bashrc 
\# --------------------------------------------------------------" >> ~/.bashrc

echo "<- Finished"

source ~/.bashrc

