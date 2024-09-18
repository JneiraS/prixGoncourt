from src.dao.base_dao import DatabaseConnectionManager
from src.utils.tables_names import TableName


class EcritDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table livres.
    """

    def __init__(self, table_name: str = TableName.ECRIT.value):
        super().__init__(table_name)
        self.table_name = table_name
