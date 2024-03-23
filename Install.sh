architecture=$(uname -m)
if [[ $architecture != *'x86_64'* ]]; then
    echo 'We only support x86_64 for now, if you want other archtecture, you can build python3.10 yourself.'
    exit
fi

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

#echo "alias yppm='python3 -m yppm'" >> ~/.bashrc
#source ~/.bashrc

if yppm about > /dev/null; then
    echo "global yppm already installed."
    exit 0
else
    echo "No yppm installed, installing now..."
fi


rm -fr /bin/yppm_folder
git clone https://gitlab.com/yingshaoxo/yppm.git /bin/yppm_folder

rm /bin/yppm
echo "python3 /bin/yppm_folder/yppm/main.py \$@" >> /bin/yppm
chmod 777 /bin/yppm


echo -e "\nYPPM Installation Finished."
echo -e "You can try it by using: yppm"
echo -e ""
echo -e "If it is not working, you have to install python3.10 by using: "
echo -e "sudo su"
echo -e "curl -sSL https://gitlab.com/yingshaoxo/use_docker_to_build_static_python3_binary_executable/-/raw/master/install.sh?ref_type=heads | bash"


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
