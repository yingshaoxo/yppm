#wget https://github.com/yingshaoxo/yppm/releases/download/v0.1/yppm -O /usr/bin/yppm 
#chmod a+rx /usr/bin/yppm 

sudo -S echo 'Working on...'

sudo rm -fr /usr/bin/yppm
sudo rm -fr /usr/bin/yppm_folder
sudo 
sudo wget https://github.com/yingshaoxo/yppm/releases/download/v0.2/yppm.tar.gz -O /root/yppm.tar.gz
sudo mkdir -p /usr/bin/yppm_folder
sudo tar -xzvf /root/yppm.tar.gz -C /usr/bin/yppm_folder
sudo 
sudo chmod a+rx /usr/bin/yppm_folder/yppm
sudo ln -s /usr/bin/yppm_folder/yppm /usr/bin/yppm
sudo chmod a+rx /usr/bin/yppm

echo 'Done'