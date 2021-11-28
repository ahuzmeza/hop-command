#! /bin/bash

# echos python shabang into hop.py
echo -n "->] Prefixing 'hop.py' with python3 shebang...|"
NEEDLE="$(which python3)"
SRC="#! /usr/local/bin/python3"
while read a; do
        echo ${a//$SRC/$NEEDLE}
done < hop.py > hop.py.t
mv hop.py{.t,}
echo "... Finished"


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


# source file to ~/.bashrc
echo -n "->] Appending source to '~/.bashrc'...|"
STRING="source $PWD/hop_shell_source"
if [ -z $(grep $STRING \~/.bashrc) ]; then
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

