# echos python shabang into hop.py
(echo "#! $(which python3)" && cat hop.py) > tmp && mv tmp hop.py
# installs pyyaml with pip
pip install pyyaml
