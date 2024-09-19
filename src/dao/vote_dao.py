from src.dao.base_dao import DatabaseConnectionManager
from src.utils.tables_names import TableName


class VoteDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table auteurs.
    """

    def __init__(self, table_name: str = TableName.VOTE.value):
        super().__init__(table_name)
        self.table_name = table_name
