# echos python shabang into hop.py
echo -n "->] prefixing hop.py with python shebang...|"
(echo "#! $(which python3)" && cat hop.py) > tmp && mv tmp hop.py
echo "... Finished"


# installs pyyaml with pip
echo "->] Installing pyyaml...\n"
pip3 install pyyaml
echo "... Finished."


# Edits shell_hop_source file to include current path as export
echo -n "->] exporting hop.py to \$PAThH...|"
while read a; do
        echo ${a//----?where?----/$PWD}
done < hop_shell_source > hop_shell_source.t
mv hop_shell_source{.t,}
echo "... Finished"



# source file to ~/.bashrc
echo -n "->] Appending source to ~/.bashrc...|"
STRING="source $PWD/hop_shell_source"
if [ -z $(grep "$STRING" ~/.bashrc) ]; then
        echo "... Skipped. Already Sourced"
else
        echo "# Hop command --------------------------------------------------
        source $PWD/hop_shell_source" >> ~/.bashrc
        echo "# --------------------------------------------------------------" >> ~/.bashrc
        echo "... Finished"
fi


# changes hop.py permission +x
echo -n "->] Setting execute permission on hop.py...|"
chmod +x hop.py
echo "... Finished"


# restarts terminal
echo -n "->] Atempting to restart terminal by sourceing bashrc...|"
source ~/.bashrc
echo "... Finished"

