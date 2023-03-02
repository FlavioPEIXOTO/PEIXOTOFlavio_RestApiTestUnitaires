Etudiant : PEIXOTO Flavio
Filière : M1 Game Programming

Le projet comporte 7 routes dont 6 intéragissant avec une base de données SQLITE contenu dans les dossiers du projet nommé "pyRestApi.db" (Il est possible de voir les informations en clair de la base de données de manière non crypté grâce à un outil de lecture tel que "TablePlus").

Deux tables sont présentes dans la base de données :
    - users
    - games


Lancement du projet :

Afin de faire fonctionner le projet voici les étapes :
    - pull le projet git
    - ouvrir un premier cmd à la racine du projet et taper la commande --> uvicorn main:app --reload
    - sur google chrome ou autre se rendre à l'adresse 127.0... donnée en console pour voir les différentes routes de l'API et tester manuellement
    - concernant les test unitaires, il faut ouvrir un second cmd à la racine du même projet et taper la commande --> python -m unittest unit\test\main_test.py

