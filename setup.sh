#! /bin/bash


# installs pyyaml with pip
echo "->] Installing pyyaml..."
pip3 install pyyaml
echo "... Finished."


# Edits shell_hop_source file to include current path as export
echo -n "->] Creating hop_shell_source...|"
echo "# HOP COMMAND ---------------------------------------------------" > hop_shell_source
echo "export PATH=\$PATH:$PWD" >> hop_shell_source
cat hop_shell_source_tmp >> hop_shell_source
echo "... Finished"


# Append sourcing file to ~/.bashrc
echo -n "->] Appending source to '~/.bashrc'...|"
STRING="/hop_shell_source"
REZ_STRING=$(grep $STRING ~/.bashrc)
echo $REZ_STRING
if [ -z "$REZ_STRING" ]; then
        echo "# Hop command --------------------------------------------------
        source $PWD/hop_shell_source" >> ~/.bashrc
        echo "# --------------------------------------------------------------" >> ~/.bashrc
        echo "... Finished"
else
        echo "... Skipped. Already Sourced"

fi


# changes hop.py permission +x
echo -n "->] Setting execute permission on 'hop.py'...|"
chmod +x hop.py
echo "... Finished"


# restarts terminal
echo -n "->] Atempting to restart terminal by sourceing '~/.bashrc'...|"
source ~/.bashrc
echo "... Finished"

