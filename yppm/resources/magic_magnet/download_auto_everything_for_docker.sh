rm -fr ~/.auto_everything/source_code
git clone https://gitlab.com/yingshaoxo/auto_everything.git ~/.auto_everything/source_code
mv ~/.auto_everything/source_code/auto_everything ./
rm -fr ~/.auto_everything/source_code

echo "Then you should rebuild docker image by using '--build' flag: sudo docker-compose -f docker-compose.light.yaml up --build"
