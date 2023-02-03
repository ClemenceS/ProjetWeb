Installation 
============

Pour utiliser notre application sans problème, il faut au préalable installer des dépendances pythons : 

.. code-block:: console

    $ pip install requirements.txt


Commande Django pour doc : 
 
.. code-block:: console

    $ pip install sphinx-rtd-theme

    $ rm genomicus/docs/source/genomApp.migrations.rst genomicus/docs/source/genomApp.rst genomicus/docs/source/genomicus.rst genomicus/docs/source/manage.rst genomicus/docs/source/member.migrations.rst genomicus/docs/source/member.rst genomicus/docs/source/modules.rst 
    $ sphinx-apidoc -o genomicus/docs/source/ genomicus/
    $ sphinx-build genomicus/docs/source/ genomicus/docs/build/