#!/bin/sh

# installs pyyaml with pip
echo "->] Installing pyyaml..."
pip3 install pyyaml
echo "... Finished.\n"

# Edits shell_hop_source file to include current path as export
echo "->] Creating hop_shell_source...|"
echo "# HOP COMMAND ---------------------------------------------------" > hop_shell_source
echo "export PATH=\$PATH:$PWD" >> hop_shell_source
cat hop_shell_source_tmp >> hop_shell_source
echo "... Finished.\n"

# changes hop.py permission +x
echo "->] Setting execute permission on 'hop.py'...|"
chmod +x hop.py
echo "... Finished.\n"

# Append sourcing file to ~/.bashrc
echo "->] Source hop_command"
if [ -z "$REZ_STRING" ]; then
        # Instructions for adding source command to shell configuration files
        echo "------------------------------------------------"
        echo "\033[1;36mTo finalize the setup, please add the following line to your shell's configuration file,"
        echo "\033[1;36mBased on your shell and OS."
        echo "\033[1;36mAdd this line:"
        echo "\033[1;33m------------------------------------------------\033[0m"
        echo "\033[0;32msource $PWD/hop_shell_source\033[0m"
        echo "\033[1;33m------------------------------------------------\033[0m"
else
        echo "... Skipped. Already Sourced"

fi

# restarts terminal
echo "\033[1;33m Remember to restart your shell session.\033[0m\n"

