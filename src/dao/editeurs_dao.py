from src.dao.base_dao import DatabaseConnectionManager
from src.dao.edit_dao import EditDAO
from src.models.editeur import Editeur
from src.utils.tables_names import TableName


class EditeursDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table livres.
    """

    def __init__(self, table_name: str = TableName.EDITEURS.value):
        super().__init__(table_name)
        self.table_name = table_name


def get_editeur_name_by_livre_id(livre_id: int) -> str:
    """
    Récupère le nom de l'editeur d'un livre.
    :param livre_id:
    :return:
    """
    edit_dao = EditDAO()
    edit_table = edit_dao.get_all()

    for edit in edit_table:
        if edit["id_livre"] == livre_id:
            for editeur in Editeur.editor_list:
                if edit["id_editeur"] == editeur.id:
                    return editeur.nom
