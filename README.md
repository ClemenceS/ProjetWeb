# Genomicus

## To run the Genomicus application

We first have to start by creating and filling the Genomicus database

### To Fill Database with the .fa data

To fill the database we have decided to use (*json*) fixtures which we create by parsing the ```.fa``` files, with a dedicated *python* script. This is not an optimal solution, but since this project consists of only a 'small' application and that we do not have a large amount of data, we felt that running these commands to create and destroy the database was a suitable option.

* To create the database, simply run the command 

```
./create_DB.sh
```


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

**Warning when pushing any changes to the git make sure to destroy the DB**

* To destroy the database, simply run the command 

```
./destroy_DB.sh
```

___

## To install the necessary python modules

Simply run the command

```
pip install -r requirements.txt
```