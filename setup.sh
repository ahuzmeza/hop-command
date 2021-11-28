# changes hop.py permission +x
echo -n "-> Setting execute permission on hop.py... "
chmod +x hop.py
echo "<- Finished"


# echos python shabang into hop.py
echo -n "-> prefixing hop.py with python shebang... "
(echo "#! $(which python3)" && cat hop.py) > tmp && mv tmp hop.py
echo "<- Finished"


# installs pyyaml with pip
echo "-> Installing pyyaml..."
pip3 install pyyaml
echo "<- Finished."


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
# --------------------------------------------------------------" > hop_shell_source
echo "<- Finished"


# source file to ~/.bashrc
echo -n "-> Appending source to ~/.bashrc... "

echo "# Hop command --------------------------------------------------
source $PWD/hop_shell_source" >> ~/.bashrc
echo "# --------------------------------------------------------------" >> ~/.bashrc

echo "<- Finished"


# restarts terminal
echo -n "-> Restarting terminal by sourceing bashrc... "
source ~/.bashrc
echo "<- Finished"
