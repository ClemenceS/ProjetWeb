[![MIT licensed](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Version 1.0.1](https://img.shields.io/badge/version-v1.0-yellow)]() [![Reproducibility](https://img.shields.io/badge/Crucial-Reproducibility-orange)]()

# Genomicus

Contributors :

* [Ambre Baumann](https://github.com/ambrebaumann)
* [Lindsay Goulet](https://github.com/Lindsay-Goulet)
* [George Marchment](https://github.com/George-Marchment)
* [Clémence Sebe](https://github.com/ClemenceS)


This repository contains :
    
* The Genomicus source code
* The Documentation
* Step by step guides to run Genomicus on a local work environnement or as a Docker container


Supervisors : 

* Bryan Brancotte
* Olivier Lespinet

___


## Steps to run Genomicus on a 'local' work environnement

### Install the necessary python modules

* We first have to start by installing the necessary python modules. Simply run the command :

```
pip install -r requirements.txt
```

### To Fill Database with the .fa data

* We have chosen to load the application with some prototype data, to create the database and fill it with the prototype data, run the command :

```
./create_DB.sh
```

To fill the database we have decided to use (*json*) fixtures which we create by parsing the ```.fa``` files, with a dedicated *python* script. This is not an optimal solution, but since this project consists of only a 'small' application and that we do not have a large amount of data, we felt that running these commands to create and destroy the database was a suitable option.

### To run the application 

* To run the Genomicus application simply run the following command

```
./run.sh
```

* To access the application, go to the following address : http://127.0.0.1:8000/ 


* To access the different users :  

| Type             | email                                       | password |
|------------------|---------------------------------------------|----------|
| 'lecteur'        | clemence.sebe@universite-paris-saclay.fr    | clemence |
| 'annotateur'     | ambre.baumann@universite-paris-saclay.fr    | ambre    |
| 'validateur'     | lindsay.goulet@universite-paris-saclay.fr   | lindsay  |
| 'administrateur' | george.marchment@universite-paris-saclay.fr | george   |

### To empty and delete the Database

>Warning : When pushing any changes to the git make sure to destroy the DB

* To destroy the database, simply run the command 

```
./destroy_DB.sh
```

___

## Steps to run Genomicus on a docker container

>Warning : When using docker, you might have to use `sudo`

### Pulling Docker image

* We first have to start by pulling the corresponding Docker image, run the command :

```
docker pull marchment/genomicus:v2.0
```

### Running the application 

* To guarantee the docker container is up to date with the current version of the genomicus project, we access the containers terminal. Simply run the following command :

```
docker run -it -p 8000:8000 --entrypoint bash  -t -i marchment/genomicus:v2.0
```

* Now we need to create the database, fill it and run the application. Simply run the following command :

```
./create_site.sh
```

* Now to access the application, go to the following address : http://localhost:8000/

>Note : To access the users, the same rule applies as above.

___
<img align="left" src="genomicus/static/logo.png" width="150">
<img align="right" src="pictures/paris-saclay.png">
