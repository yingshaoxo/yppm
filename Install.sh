#if which curl >/dev/null; then
#    echo "curl is installed."
#else
#    echo "curl is not installed. Installation Failed."
#    exit 0
#fi

if which git >/dev/null; then
    echo "git is installed."
else
    echo "git is not installed. Installation Failed."
    exit 0
fi

if which python3 >/dev/null; then
    #the_real_py_command="python3"
    echo "python3 is installed."
else
    echo "python3 is not installed. Installation Failed."
    exit 0
fi

#if $the_real_py_command -m pip >/dev/null; then
#    echo "pip is installed."
#else
#    curl -sSL https://bootstrap.pypa.io/get-pip.py | $the_real_py_command
#fi

#if $the_real_py_command -m pip show yppm > /dev/null; then
#    echo "python package yppm installed."
#else
#    $the_real_py_command -m pip install yppm --break-system-packages
#    #$the_real_py_command -m pip install "git+https://github.com/yingshaoxo/yppm.git@main"
#fi

if yppm about > /dev/null; then
    echo "global yppm already installed."
    exit 0
else
    echo "No yppm installed, installing now..."
    #echo "alias yppm='python3 -m yppm'" >> ~/.bashrc
    #source ~/.bashrc
fi


rm -fr /bin/yppm_folder
git clone https://gitlab.com/yingshaoxo/yppm.git /bin/yppm_folder

rm /bin/yppm
echo "python3 /bin/yppm_folder/yppm/main.py $@" >> /bin/yppm
chmod 777 /bin/yppm


echo -e "\nYPPM Installation Finished."
echo -e "You can try it by using: yppm"


# Method 1
#wget https://github.com/yingshaoxo/yppm/releases/download/v0.1/yppm -O /usr/bin/yppm 
#chmod a+rx /usr/bin/yppm 

# Method 2
#if which wget >/dev/null; then
#    echo "wget is installed."
#else
#    echo "wget is not installed. Installation Failed."
#    exit 0
#fi
#
#if which tar >/dev/null; then
#    echo "tar is installed."
#else
#    echo "tar is not installed. Installation Failed."
#    exit 0
#fi
#
#echo 'Working on...'
#
#rm -fr /usr/bin/yppm
#rm -fr /usr/bin/yppm_folder
#
#wget https://github.com/yingshaoxo/yppm/releases/download/v0.3/yppm.tar.gz -O /root/yppm.tar.gz
#mkdir -p /usr/bin/yppm_folder
#tar -xzvf /root/yppm.tar.gz -C /usr/bin/yppm_folder
#
#chmod a+rx /usr/bin/yppm_folder/yppm
#ln -s /usr/bin/yppm_folder/yppm /usr/bin/yppm
#chmod a+rx /usr/bin/yppm
#
#echo 'Done'
