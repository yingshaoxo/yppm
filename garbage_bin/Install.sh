# Install python3
ln -s "$(which python)" "/usr/bin/python3"

# Install pip
curl https://bootstrap.pypa.io/get-pip.py | python3
python3 -m ensurepip --upgrade

# Install auto_everything
export PIP_BREAK_SYSTEM_PACKAGES=1
python3 -m pip uninstall auto_everything -y
python3 -m pip install "git+https://github.com/yingshaoxo/auto_everything.git@dev"

# Install yppm
rm -fr ~/.yppm
git clone https://github.com/yingshaoxo/yppm.git ~/.yppm
sudo cp ~/.yppm/yppm.sh /usr/bin/yppm
sudo chmod 777 /usr/bin/yppm

# Welcome
clear
echo -e "Welcome to use yppm.\n\nYou can run 'yppm' to create a new Python project."