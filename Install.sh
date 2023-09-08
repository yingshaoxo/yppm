#wget https://github.com/yingshaoxo/yppm/releases/download/v0.1/yppm -O /usr/bin/yppm 
#chmod a+rx /usr/bin/yppm 

echo 'Working on...'

rm -fr /usr/bin/yppm
rm -fr /usr/bin/yppm_folder

wget https://github.com/yingshaoxo/yppm/releases/download/v0.2/yppm.zip -O /root/yppm.tar.gz
mkdir -p /usr/bin/yppm_folder
tar -xzvf /root/yppm.tar.gz -C /usr/bin/yppm_folder

chmod a+rx /usr/bin/yppm_folder/yppm
ln -s /usr/bin/yppm_folder/yppm /usr/bin/yppm
chmod a+rx /usr/bin/yppm

echo 'Done'