from src.dao.base_dao import DatabaseConnectionManager
from src.models.livre import Livre

from src.utils.tables_names import TableName


class AppartientDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table appartient.
    """

    def __init__(self, table_name: str = TableName.APPARTIENT.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_selection(self, selection: int) -> list[dict]:
        query: str = (
            f"SELECT * FROM `{TableName.APPARTIENT.value}` WHERE `id_selection` = {selection}"
        )
        results: list[dict] = self.query_database(query)
        return results

    def get_books_in_selection(self, selection: int) -> list[Livre]:
        """
        Récupère tous les livres d'une sélection spécifique.

        Cette méthode utilise l'objet DAO Appartient pour obtenir les livres
        associés à une sélection donnée et les retourne sous forme de liste.
        :param selection: l'identifiant de la selection
        :return:
        """
        second_selection_list: list = []
        results: list[dict] = self.get_selection(selection)
        for result in results:
            for book in Livre.book_list:
                if result["id_livre"] == book.id:
                    second_selection_list.append(book)
        return second_selection_list

    def insert_book_to_selection(self, id_livre: int, id_selection: int):
        """
        Insère un livre dans une collection spécifique.
        Cette méthode utilise l'objet DAO Appartient pour insérer une entrée
        dans la table.

        :param id_livre:
        :param id_selection:
        """
        self.create(
            f"INSERT INTO `{TableName.APPARTIENT.value}` (`id_livre`, `id_selection`) VALUES "
            f"('{id_livre}', '{id_selection}')"
        )
