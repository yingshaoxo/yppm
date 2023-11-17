# magic_magnet
A torrent client that implements yingshaoxo torrent protocol.

> 'ytorrent' is a protocol. 'magic_magnet' is a software.


## Yingshaoxo Torrent Protocol

1. For all those clients, it will need at least one tracker service. That service has an public ip address. It only need to have one open port.

2. When a client open a new torrent, I mean seeding. That client will do a report to the tracker with the following infomation: {"has_public_ip": "*.*.*.*", "hash": "", "size": 100}

3. When a client want to download a file with certain hash from a magnet link, it will do a asking to the tracker. If the tracker found there has a resource that matchs the hash code, if the seeder has public ip address, then it will let the client do a download directly from that seeder, otherwise, if that seeder does not have an public ip address, then the tracker will ask the seeder to upload its resources first, then transfer it to the client that asks the resources.

## For the python command line software
### Installation
It should be a server, and also a client.

It should as simple as:
```
1. Install python3.10 by using some command.
2. Put "python3.10 main.py" bash script as file "magic_magnet" under "/usr/bin".
3. Use "sudo chmod 777 /usr/bin/magic_magnet" to let "magic_magnet" global accessble.
```

### Usage
When you run `magic_magnet *` the first time, it will start a server, which gives you a tracker url/ip address

When you run `magic_magnet search/seed keywords/path` again, it will check if the local service is running or not, if it isn't, it will try to launch it again, otherwise, it will do the right job you ask

#### Command List
* magic_magnet * 
* magic_magnet enable user_interface
* magic_magnet seed <folder_file_path>
* magic_magnet search <keywords>
* magic_magnet download <magnet_magic_link>
* magic_magnet stop

### Configurations
~/.ytorrent/configuration.json
```json
{
    "default_remote_service_port": 1111,
    "seeder_tracker_address": None,
    "default_local_service_port": 1212,
    "file_segments_memory_pool_size_in_mb": 500,
    "max_acceptable_file_segment_size_in_mb": 2,
    "polling_waiting_time_in_seconds": 60,
    "tracker_ip_or_url_list": [],
    "download_folder_path": "~/Downloads/Ytorrent_Download"
}
```

~/.ytorrent/tracker_urls.txt
```
https://ytorrent.xx.com
https://ytorrent.yy.com
...
```

### How to build a binary file from docker
```
sudo docker-compose -f docker-compose.magic_magnet_python.yaml up --build

cd data/magic_magnet
sudo chown -R $(whoami):$(whoami) .
sudo chmod g+rw .
```

### For the electron app
It should spawn the about python software and execute it first with "enable user_interface", then launch the user interface written by vue3(vite).

<!-- ## How to compile it?

```
sudo docker-compose -f docker-compose.magic_magnet.yaml up --build
```

If anything goes wrong, you may want to get into the docker container to fix it:
```
sudo docker exec -it --user=root 3d86fb657430 /bin/sh
``` -->
