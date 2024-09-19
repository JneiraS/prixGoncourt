from src.dao.base_dao import DatabaseConnectionManager

from src.utils.tables_names import TableName


class MembresJuryDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table livres.
    """

    def __init__(self, table_name: str = TableName.MEMBER_JURY.value):
        super().__init__(table_name)
        self.table_name = table_name

    def gethash(self) -> list[dict]:
        """
        Récupère les Hash des membres dans la base de données.
        """
        query = f"SELECT * FROM {self.table_name}"
        results: list[dict] = self.query_database(query)

        return results
