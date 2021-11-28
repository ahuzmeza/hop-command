#! /bin/bash


# installs pyyaml with pip
echo "->] Installing pyyaml..."
pip3 install pyyaml
echo "... Finished."


# Edits shell_hop_source file to include current path as export
echo -n "->] Exporting 'hop.py' to \$PAThH...|"
while read a; do
        echo ${a//----?where?----/$PWD}
done < hop_shell_source > hop_shell_source.t
mv hop_shell_source{.t,}
echo "... Finished"


# Append sourcing file to ~/.bashrc
echo -n "->] Appending source to '~/.bashrc'...|"
STRING="/hop_shell_source"
REZ_STRING=$(grep $STRING ~/.bashrc)
echo "--------------------------------"
echo $REZ_STRING
echo "--------------------------------"
if [ -z REZ_STRING ]; then
        echo "... Skipped. Already Sourced"
else
        echo "# Hop command --------------------------------------------------
        source $PWD/hop_shell_source" >> ~/.bashrc
        echo "# --------------------------------------------------------------" >> ~/.bashrc
        echo "... Finished"
fi


# changes hop.py permission +x
echo -n "->] Setting execute permission on 'hop.py'...|"
chmod +x hop.py
echo "... Finished"


# restarts terminal
echo -n "->] Atempting to restart terminal by sourceing '~/.bashrc'...|"
source ~/.bashrc
echo "... Finished"

