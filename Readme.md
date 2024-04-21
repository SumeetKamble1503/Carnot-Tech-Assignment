# Carnot Technologies Assignment

This project contains two services.
1. Backend (Flask App)
2. Redis (Redis Cache Database)


## Installation

You'll need docker and docker-compose installed.


### Installing docker
`sudo apt update`

`sudo apt install apt-transport-https ca-certificates curl software-properties-common`

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`

`sudo apt install docker-ce`

`sudo systemctl status docker`

>Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running

You can refer to this if any more issues prevail,
[Digital Ocean Install docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)


### Installing docker-compose

`sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

`sudo chmod +x /usr/local/bin/docker-compose`

`docker-compose --version`

>docker-compose should be installed

You can refer to this if any more issues prevail,
[Digital Ocean Install docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)


## Commands to run and build the application

`docker-compose -f docker-compose.yml up --build -d`

>This will build and run the application

`docker-compose -f docker-compose.yml logs -f <service_name>`

>This command will show you logs of that service


## Postman Collection

You can download the Postman collection [here](https://drive.google.com/file/d/1_-Ch3APrhBArg6yred_-UU4g1BsqC5dO/view?usp=sharing)
Just replace the IPv4 address with `localhost` to hit the APIs


## Redis DB

To visually view the Redis database.
You'll need to setup P3X for Linux.
For Windows you can download [Redis Insight](https://redis.io/insight/)

