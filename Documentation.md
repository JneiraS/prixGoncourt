# Conception de la DB
## MCD
     
![MCD](https://raw.githubusercontent.com/JneiraS/prixGoncourt/refs/heads/develop/Evaluation_MCD.png)
## MLD
     
![MLD](https://raw.githubusercontent.com/JneiraS/prixGoncourt/refs/heads/develop/Evaluation_MLD.png)

# Diagramme de Classe

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://raw.githubusercontent.com/JneiraS/prixGoncourt/refs/heads/develop/D_Class%20UML.jpg)
## Gestion des DAO

- Les classes **DAO (Data Access Object)** héritent toutes de la classe `DatabaseConnectionManager`, qui assure la gestion des connexions à la base de données et fournit des méthodes utilitaires.

- `SingletonMeta`

  - Une métaclasse utilisée pour transformer des classes en **singleton**, garantissant qu'une seule instance de la classe existe.

  - **Méthodes**

  - **call** : Utilise un verrou (`Lock`) pour garantir qu'une seule instance de la classe est créée, même dans un environnement multithread.

    ---

- `DatabaseConnectionManager`

  - Cette classe gère l'ouverture et la fermeture des connexions avec la base de données et fournit des méthodes utilitaires pour exécuter des requêtes SQL.

  - **init(self, table_name: str)**

  - **Paramètre** :

    - `table_name` : Nom de la table associée à ce gestionnaire de connexion.

  - **Méthodes**

  - **open_connection(self)** : Ouvre une connexion avec la base de données en utilisant un fichier de configuration JSON.

  - **close_connection(self)** : Ferme la connexion et le curseur associé.

  - **get_all(self, limit: int = None, offset: int = None)** : Récupère tous les enregistrements d'une table avec option de pagination.

  - **create(self, query: str)** : Insère une nouvelle entrée dans la base de données et retourne l'ID généré.

  - **read(self, identifier: int)** : Récupère une entrée spécifique à partir de son identifiant.

  - **update(self, table)** : Met à jour une entrée dans la base de données (méthode non implémentée).

  - **delete(self, id_to_delete: int)** : Supprime une entrée à partir de son ID.

  - **insert_and_get_id(self, query: str)** : Exécute une requête d'insertion et retourne l'ID de l'entité nouvellement créée.

  - **query_database(self, query: str)** : Exécute une requête SQL et retourne les résultats sous forme de liste de dictionnaires.

  - **run_query_with_commit(self, query: str)** : Exécute une requête avec validation de la transaction.

    ---

- **AppartientDAO**

  - Gère la table `appartient`, qui relie les livres aux sélections.
  - **Méthodes**
  - **get_selection(self, selection: int)** : Récupère tous les enregistrements pour une sélection spécifique.
  - **get_books_in_selection(self, selection: int)** : Retourne une liste d'objets `Livre` pour une sélection donnée.
  - **insert_book_to_selection(self, id_livre: int, id_selection: int)** : Insère un livre dans une sélection.
  - **add_books_to_selection(self, selection_id: int, results_list: list[int])**: Ajoute tous les livres d'une liste à une selection
  - **get_current_round(self)**: renvoie le tour actuel

- **VoteDAO**

  - Gère la table `vote`, qui enregistre les votes pour les livres.

  - **Méthodes**

  - **get_voting_results_for(self, round_vote: int, length_of_selection: int)** : Récupère les résultats des votes pour une ronde donnée.

  - **count_votes(id_livre: int, round_vote: int)** : Compte le nombre de votes pour un livre donné lors d'une ronde spécifique.

  - **send_all_votes_to_db(self, choices: list, id_member: int, vote_round: int)**: Enregistre les votes dans la base de données

    ---

- **AuteursDAO**

  - Gère la table `auteurs`, contenant les informations des auteurs.

  - **Méthodes**

  - **init(self, table_name: str = TableName.AUTEURS.value)** : Initialise l'objet DAO avec la table `auteurs`.

    ---

- **EcritDAO**

  - Gère la table `ecrit`, qui enregistre les relations entre les auteurs et les livres.

  - **Méthodes**

  - **get_auteur_by_livre_id(self, livre_id: int)** : Récupère l'auteur d'un livre donné en fonction de son identifiant.

    ---

- **EditDAO**

  - Gère la table `edit`, qui relie les éditeurs aux livres.
  - **Méthodes**
  - **get_editeur_name_by_livre_id(self, livre_id: int)** : Récupère le nom de l'éditeur d'un livre en fonction de son identifiant.

  ---

- **EditeursDAO**

  - Gère la table `editeurs`, qui contient les informations des éditeurs.

  - **Méthodes**

  - **init(self, table_name: str = TableName.EDITEURS.value)** : Initialise l'objet DAO avec la table `editeurs`.

    ---

- **LivresDAO**

  - Gère la table `livres`, qui contient les informations des livres.

  - **Méthodes**

  - **init(self, table_name: str = TableName.LIVRES.value)** : Initialise l'objet DAO avec la table `livres`.

    ---

- **MembresJuryDAO**

  - Gère la table `member_jury`, qui enregistre les membres du jury.

  - **Méthodes**

  - **gethash(self)** : Récupère les `hash` des membres du jury dans la base de données.

    ---

- **PersonnagesDAO**

  - Gère la table `personnages`, qui contient les informations sur les personnages.
  - **init(self, table_name: str = TableName.PERSONNAGES.value)**
  - Initialise l'objet DAO avec la table `personnages`.

---

- **Conclusion**
  - Chaque DAO fournit des méthodes spécifiques pour interagir avec sa table respective. Les opérations de base incluent la récupération des données (`get_all`, `read`), l'insertion (`create`), et la suppression (`delete`). La gestion des connexions est centralisée dans `DatabaseConnectionManager`, garantissant une interface cohérente pour accéder à la base de données.

---

## Modèles d'Entités

- Toutes ces entités héritent de la classe abstraite `Entity`, qui définit un modèle commun pour chaque entité avec un identifiant unique. Les entités incluent des auteurs, éditeurs, livres, membres du jury et personnages.

- `Entity` **(Classe Abstraite)**

  - La classe `Entity` est une **interface abstraite** qui définit un modèle de base pour toutes les entités du système. Elle impose que chaque entité ait un identifiant unique (`id`).

  - **init(self)**

  - **Description** : Constructeur abstrait. Les classes filles sont obligées de définir un identifiant (`id`).

  - **Propriétés**

  - **id (getter)** : Retourne l'identifiant unique de l'entité.

  - **id (setter)** : Définit l'identifiant unique de l'entité. Vérifie que la valeur assignée est un entier ou `None`.

    - **Exceptions** : Lève une `ValueError` si la valeur n'est pas un entier ou `None`.

      ---

- `Auteur`

  - La classe `Auteur` représente un auteur et hérite de `Entity`. Chaque auteur est défini par son nom et sa biographie. Une liste `auteur_list` stocke tous les objets créés.

  - **init(self, nom: str, biographie: str)**

  - **Paramètres** :

    - `nom` : Le nom de l'auteur.
    - `biographie` : Une description biographique de l'auteur.

  - **Attributs**

  - `nom` : Le nom de l'auteur.

  - `biographie` : La biographie de l'auteur.

  - **Classe** : `auteur_list` : Liste contenant tous les auteurs créés.

    ---

- `Editeur`

  - La classe `Editeur` représente un éditeur et hérite de `Entity`. Chaque éditeur est défini par son nom. Une liste `editor_list` stocke tous les éditeurs créés.

  - **init(self, nom: str)**

  - **Paramètre** :

    - `nom` : Le nom de l'éditeur.

  - **Attributs**

  - `nom` : Le nom de l'éditeur.

  - **Classe** : `editor_list` : Liste contenant tous les éditeurs créés.

    ---

- `Livre`

  - La classe `Livre` représente un livre et hérite de `Entity`. Chaque livre est défini par son titre, résumé, date de publication, nombre de pages, ISBN et prix. Une liste `book_list` stocke tous les livres créés.

  - **init(self, title: str, summary: str, publication_date: date, number_of_pages: int, isbn: str, price: float)**

  - **Paramètres** :

    - `title` : Le titre du livre.
    - `summary` : Un résumé du livre.
    - `publication_date` : La date de publication.
    - `number_of_pages` : Le nombre de pages du livre.
    - `isbn` : L'ISBN du livre.
    - `price` : Le prix du livre.

  - **Attributs**

  - `title` : Le titre du livre.

  - `summary` : Le résumé du livre.

  - `publication_date` : La date de publication.

  - `number_of_pages` : Le nombre de pages.

  - `isbn` : Le numéro ISBN.

  - `price` : Le prix du livre.

  - **Classe** : `book_list` : Liste contenant tous les livres créés.

    ---

- `MembreJury`

  - La classe `MembreJury` représente un membre du jury et hérite de `Entity`. Chaque membre est défini par son nom et son rôle.

  - **init(self, nom: str, role: str)**

  - **Paramètres** :

    - `nom` : Le nom du membre du jury.
    - `role` : Le rôle du membre dans le jury.

  - **Attributs**

  - `nom` : Le nom du membre du jury.

  - `role` : Le rôle du membre du jury.

    ---

- `Personnage`

  - La classe `Personnage` représente un personnage et hérite de `Entity`. Chaque personnage est défini par son nom et son rôle.

  - **init(self, nom: str, role: str)**

  - **Paramètres** :

    - `nom` : Le nom du personnage.
    - `role` : Le rôle du personnage dans l'histoire.

  - **Attributs**

  - `nom` : Le nom du personnage.

  - `role` : Le rôle du personnage.

    ---

- **Utilisation Commune**

  - Chaque classe représente une entité distincte avec un identifiant unique, qui est géré par la classe mère `Entity`. Les classes `Auteur`, `Editeur`, `Livre`, `MembreJury`, et `Personnage` héritent de cette structure commune et sont utilisées pour modéliser leurs entités respectives dans un système de gestion de base de données.

  ---

## `Creator` et Création d'Objets depuis la Base de Données

- Cette partie  décrit le fonctionnement de la classe abstraite `Creator`, ses sous-classes concrètes qui créent des objets spécifiques à partir d'une source d'information, ainsi que les fonctions qui permettent de récupérer et créer des objets depuis la base de données en utilisant un mécanisme multi-threading.

### `Creator` **(Classe Abstraite)**

- Description

  La classe `Creator` est une **classe abstraite** qui définit une méthode de **factory** (`factory_method`) pour créer des objets. Elle sert de modèle pour la création d'objets spécifiques dans les classes dérivées.

### **factory_method(self, information_source)**

- **Description** : Méthode abstraite qui doit être implémentée par les sous-classes. Elle prend une source d'information (souvent sous forme de dictionnaire) et crée un objet à partir de cette source.
- **Paramètre** :
  - `information_source` : Les données nécessaires pour créer un objet.
- **Retour** : None (implémentée dans les sous-classes concrètes).

  ---

### Sous-classes de `Creator`

Les sous-classes concrètes implémentent la méthode `factory_method` pour créer des instances spécifiques d'objets tels que `Livre`, `Auteur`, `Editeur`, `MembreJury`, et `Personnage`.

- `LivresCreator`

  - Crée des instances de `Livre`.

    **factory_method(self, information_source: dict) -&gt; Livre**
    - **Paramètre** : Un dictionnaire contenant les informations nécessaires pour créer un objet `Livre` (titre, résumé, date de publication, etc.).
    - **Retour** : Une instance de `Livre`.

- `AuteursCreator`

  - Crée des instances de `Auteur`.

    **factory_method(self, information_source: dict) -&gt; Auteur**
    - **Paramètre** : Un dictionnaire contenant les informations nécessaires pour créer un objet `Auteur` (nom, biographie).
    - **Retour** : Une instance de `Auteur`.

- `EditeursCreator`

  - Crée des instances de `Editeur`.

    **factory_method(self, information_source: dict) -&gt; Editeur**
    - **Paramètre** : Un dictionnaire contenant le nom de l'éditeur.
    - **Retour** : Une instance de `Editeur`.

- `MembreJuryCreator`

  - Crée des instances de `MembreJury`.

    **factory_method(self, information_source: dict) -&gt; MembreJury**
    - **Paramètre** : Un dictionnaire contenant le nom et le rôle d'un membre du jury.
    - **Retour** : Une instance de `MembreJury`.

- `PersonnagesCreator`

  - Crée des instances de `Personnage`.

    **factory_method(self, information_source: dict) -&gt; Personnage**
    - **Paramètre** : Un dictionnaire contenant le nom et le rôle d'un personnage.

    - **Retour** : Une instance de `Personnage`.

      ---

### Fonctions de Création à partir de la Base de Données

Ces fonctions permettent de récupérer des objets depuis la base de données en utilisant leurs DAO respectifs et de les transformer en objets Python en utilisant les classes de création (creators).

- `create_all_personnages_from_database()`

  - **Description** : Récupère tous les personnages de la base de données via `PersonnagesDAO` et retourne une liste d'objets `Personnage`.
  - **Retour** : Une liste d'objets `Personnage`.

- `create_all_membre_jury_from_database()`

  - **Description** : Récupère tous les membres du jury depuis la base de données via `MembresJuryDAO` et retourne une liste d'objets `MembreJury`.
  - **Retour** : Une liste d'objets `MembreJury`.

- `create_all_editeurs_from_database()`

  - **Description** : Récupère tous les éditeurs de la base de données via `EditeursDAO` et retourne une liste d'objets `Editeur`.
  - **Retour** : Une liste d'objets `Editeur`.

- `create_all_livres_from_database()`

  - **Description** : Récupère tous les livres de la base de données via `LivresDAO` et retourne une liste d'objets `Livre`.
  - **Retour** : Une liste d'objets `Livre`.

- `create_all_auteurs_from_database()`

  - **Description** : Récupère tous les auteurs de la base de données via `AuteursDAO` et retourne une liste d'objets `Auteur`.
  - **Retour** : Une liste d'objets `Auteur`.

    ---

`initialize_database_in_threads()`

- **Description**

  - Cette fonction initialise la création des objets (`Auteur`, `Editeur`, `Livre`, `MembreJury`, `Personnage`) depuis la base de données **en parallèle** à l'aide de threads, pour optimiser les performances.

- **Mécanisme**

  - Utilise `concurrent.futures.ThreadPoolExecutor` pour exécuter chaque fonction de création dans un thread séparé.
  - Cela permet de récupérer simultanément tous les types d'objets sans bloquer le processus principal.

- **Processus**

  - Les fonctions de création (`create_all_auteurs_from_database`, `create_all_editeurs_from_database`, etc.) sont exécutées en parallèle.

    ---

- **Conclusion**

  - Le `Creator` est une implémentation du **Factory Method Pattern**, qui permet de créer différents types d'objets à partir de données. Les fonctions de création accèdent à la base de données, récupèrent les enregistrements via des DAO, puis les transforment en objets Python. Le processus de création est optimisé via le multi-threading, permettant un chargement simultané des données.

  ---


- `Authentication`collapsed:: true

  - **Classe** `Authentication`

    - La classe `Authentication` permet de gérer l'authentification d'un membre du jury en vérifiant un mot de passe avec un mécanisme de hachage. Elle inclut des méthodes pour hasher un mot de passe, le vérifier par rapport à la base de données, et supprimer l'objet d'authentification une fois le processus terminé.

  - **init(self, password: str)**

    - Le constructeur initialise une instance d'`Authentication` avec un mot de passe en clair fourni par l'utilisateur.

  - **Paramètre :**

    - `password` : Le mot de passe en clair à hacher et vérifier.

      ---

  - **Méthodes de** `Authentication`

  - **hash_password(self) -&gt; str**

    Retourne le mot de passe haché en utilisant l'algorithme **SHA-256**.

  - **Description** : Cette méthode prend le mot de passe en clair, le convertit en une chaîne de caractères hachée via **SHA-256**.

  - **Retour** : Le mot de passe haché sous forme de chaîne hexadécimale.

    ---

  - **check_password(self) -&gt; dict**

    Vérifie si le mot de passe donné correspond à un mot de passe stocké dans la base de données.

  - **Description** : Cette méthode hache le mot de passe donné et le compare aux mots de passe stockés dans la base de données, récupérés via `MembresJuryDAO`. Si une correspondance est trouvée, elle retourne les informations associées au membre du jury.

  - **Retour** : Un dictionnaire contenant les informations du membre du jury si le mot de passe est correct. Sinon, `None`.

    ---

  - **delete_auth(self)**

    - Supprime l'objet d'authentification en utilisant l'instruction `del`. Cette méthode est utilisée pour nettoyer les informations sensibles après la vérification de l'authentification.

  - **Description** : Supprime l'objet `Authentication` afin de libérer la mémoire et d'éliminer toute trace du mot de passe.

    ---

  - **Fonction** `authenticate()`

  - Description

    La fonction `authenticate` gère le processus d'authentification d'un membre du jury en demandant un mot de passe à l'utilisateur et en vérifiant sa validité en utilisant la classe `Authentication`.

    - **Processus**
      1. Demande à l'utilisateur de saisir son mot de passe via la bibliothèque `rich` qui masque l'entrée du mot de passe.
      2. Crée une instance d'`Authentication` avec le mot de passe saisi.
      3. Appelle la méthode `check_password` pour vérifier si le mot de passe est correct.
      4. Si le mot de passe est correct, retourne les informations du membre du jury, sinon `None`.
    - **Retour :**
      - Un dictionnaire contenant les informations du membre du jury si l'authentification est réussie. Sinon, `None`.

        ---

  - **Intégration avec** `MembresJuryDAO`

    La classe `Authentication` dépend de `MembresJuryDAO` pour récupérer les mots de passe hachés des membres du jury à partir de la base de données.

  - `MembresJuryDAO.gethash()` : Cette méthode retourne une liste de dictionnaires contenant les mots de passe hachés des membres du jury.

    ---

  - **Conclusion**

    - La classe `Authentication` implémente un mécanisme simple et sécurisé d'authentification des membres du jury via le hachage des mots de passe. L'authentification est réalisée en hachant le mot de passe entré par l'utilisateur et en le comparant avec ceux stockés dans la base de données. La fonction `authenticate()` facilite ce processus pour l'utilisateur.

    ---

- `TableName` **Enum** et **Fonction `read_json` **collapsed:: true

  - `TableName` **Enum**

    - Description

      `TableName` est une énumération (classe `Enum`) qui stocke les noms des tables de la base de données. Cela permet d'utiliser des noms de tables standardisés dans tout le code, évitant les erreurs causées par les chaînes de caractères en dur.

    - Valeurs de l'énumération

    - **LIVRES** : Représente la table des livres (`"livres"`).

    - **AUTEURS** : Représente la table des auteurs (`"auteurs"`).

    - **EDITEURS** : Représente la table des éditeurs (`"editeurs"`).

    - **MEMBER_JURY** : Représente la table des membres du jury (`"membre_jury"`).

    - **PERSONNAGES** : Représente la table des personnages (`"personnages"`).

    - **EDIT** : Représente la table des relations entre éditeurs et livres (`"edit"`).

    - **ECRIT** : Représente la table des relations entre auteurs et livres (`"ecrit"`).

    - **APPARTIENT** : Représente la table des relations entre sélections et livres (`"appartient"`).

    - **VOTE** : Représente la table des votes (`"vote"`).

      ---

  - `read_json` **Function**

    - **Description**

      - La fonction `read_json` lit un fichier JSON à partir du chemin fourni et retourne son contenu sous forme de dictionnaire Python.

    - **Paramètres** :

      - `file_name` (str) : Le chemin du fichier JSON à lire.

    - **Retour** :

      - **dict** : Retourne le contenu du fichier JSON sous forme de dictionnaire.

    - **Exceptions** :

      - **FileNotFoundError** : Lève une erreur si le fichier n'est pas trouvé.

    - **Gestion des erreurs** :

      - Si le fichier JSON n'existe pas, un message d'erreur est imprimé et l'exception `FileNotFoundError` est levée.

        ---

  - Conclusion

    - `TableName` : Simplifie l'accès aux noms des tables de la base de données, réduisant les risques d'erreurs lors de l'écriture des requêtes SQL.
    - `read_json` : Permet une gestion facile et centralisée des fichiers de configuration ou de données au format JSON.

      ---

    
