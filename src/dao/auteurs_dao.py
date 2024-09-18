from src.dao.base_dao import DatabaseConnectionManager
from src.dao.ecrit_dao import EcritDAO
from src.models.auteur import Auteur
from src.utils.tables_names import TableName


class AuteursDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table auteurs.
    """

    def __init__(self, table_name: str = TableName.AUTEURS.value):
        super().__init__(table_name)
        self.table_name = table_name


def get_auteur_by_livre_id(livre_id: int) -> str:
    """
    Récupère l'auteur d'un livre dans la base de données.
    """
    ecrit_dao = EcritDAO()
    ecrit_table = ecrit_dao.get_all()

    for ecrit in ecrit_table:
        if ecrit["id_livre"] == livre_id:
            for auteur in Auteur.auteur_list:
                if ecrit["id_auteur"] == auteur.id:
                    return auteur.nom
