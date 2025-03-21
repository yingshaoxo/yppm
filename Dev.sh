if yppm about > /dev/null; then
    echo "global yppm already installed."
    exit 0
else
    echo "No yppm installed, installing now..."
fi

rm -fr /bin/yppm_folder
cp -fr . /bin/yppm_folder
chmod +r /bin/yppm_folder/yppm/main.py
chmod +rx /bin/yppm_folder

rm /bin/yppm
echo "python3 /bin/yppm_folder/yppm/main.py \$@" >> /bin/yppm
#vim "python3 /bin/yppm_folder/yppm/main.py $@" >> /bin/yppm
chmod 777 /bin/yppm


echo -e "\nYPPM Installation Finished."
echo -e "You can try it by using: yppm"
echo -e ""
echo -e "If it is not working, you have to install python3.10 by using: "
echo -e "sudo su"
echo -e "curl -sSL https://gitlab.com/yingshaoxo/use_docker_to_build_static_python3_binary_executable/-/raw/master/install.sh?ref_type=heads | bash"
