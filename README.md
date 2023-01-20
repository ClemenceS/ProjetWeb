# Genomicus

## To Fill Database with the .fa data

To fill the database we have decided to use (*json*) fixtures which we create by parsing the ```.fa``` files, with a dedicated *python* script. This is not an optimal solution, but since this project consists of only a 'small' application and that we do not have a large amount of data, we felt that running these commands to create and destroy the database was a suitable option.

**Warning when pushing any changes to the git make sure to destroy the DB**

* To create the database, simply run the command 

```
./create_DB.sh
```

* To destroy the database, simply run the command 

```
./destroy_DB.sh
```


## To install the necessary python modules

Simply run the command

```
pip install -r requirements.txt
```