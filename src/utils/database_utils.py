import json

from src.utils.logger import logger, LogMessages


def read_json(file_name: str) -> dict:
    """
    Lit un fichier json et le retourne sous forme de dictionnaire.
    :param file_name:
    :return: Un dictionnaire contenant le contenu du fichier
    """
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Erreur: Le fichier {file_name} n'a pas été trouvé.")
        raise e


def insert_and_get_id(self, query: str) -> int | None:
    """
    Insère une nouvelle valeur dans la base de données et retourne son identifiant.
    :param self:
    :param query:  La requête SQL
    :return: identifiant de la nouvelle entité
    """
    logger.debug(LogMessages.DEBUG_MESSAGE.value)
    try:
        self.open_connection()
        self.cursor.execute(query)
        id_generated = self.cursor.lastrowid
        self.conn.commit()
        self.close_connection()
        logger.info(f"Fonction: {run_query_with_commit.__name__} terminée avec succès")

        return id_generated

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        self.close_connection()
        logger.error(f"Erreur lors de l'exécution : {str(e)}")
        return None


def query_database(self, query: str) -> list[dict] | None:
    """
    Exécute une requête SQL et renvoie les résultats sous forme de liste de dictionnaires.
    :param self:
    :param query: la requête SQL
    :return: liste de dictionnaires ou None
    """
    logger.debug(LogMessages.DEBUG_MESSAGE.value)
    try:
        self.open_connection()
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.close_connection()
        logger.info(f"Fonction: {run_query_with_commit.__name__} terminée avec succès")

        return rows

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        self.close_connection()
        logger.error(f"Erreur lors de l'exécution : {str(e)}")
        return None


def run_query_with_commit(self, query: str):
    """
    Exécute une requête SQL et valide la transaction.
    :param self:
    :param query: la requête SQL
    :return: True si la requête a été exécutée correctement, False sinon
    """
    logger.debug(LogMessages.DEBUG_MESSAGE.value)

    try:
        self.open_connection()
        self.cursor.execute(query)
        self.conn.commit()
        self.close_connection()
        logger.info(f"Fonction: {run_query_with_commit.__name__} terminée avec succès")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Erreur lors de l'exécution : {str(e)}")
        self.close_connection()
        return False
