# installs pyyaml with pip
echo "-> Installing pyyaml..."
pip3 install pyyaml
echo "-> Finished."


# creates shell_hop_source file
echo "-> Creating shell_hop_source file..."

echo "\n# Hop command --------------------------------------------------
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
echo "-> Finished"

# source file to ~/.bashrc
echo "-> Appending source to ~/.bashrc..."

echo "\n# Hop command --------------------------------------------------" >> ~/.bashrc 
echo "source $PWD/hop_shell_source" >> ~/.bashrc 
echo "# --------------------------------------------------------------\n" >> ~/.bashrc

echo "-> Finished"

source ~/.bashrc

