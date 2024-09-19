from src.dao.base_dao import DatabaseConnectionManager
from src.utils.tables_names import TableName


class VoteDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table auteurs.
    """

    def __init__(self, table_name: str = TableName.VOTE.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_voting_results_for(self, round_vote: int):
        """
        Renvoie les résultats de vote pour une tour de vote donnée.
        :param round_vote: l'identifiant de la ronde de vote
        :return: la liste des identifiants des livres qui ont  t  choisis
        """
        return self.query_database(
            f"SELECT `id_livre` FROM `{self.table_name}` WHERE `id_selection` = {round_vote}"
        )


def count_votes(id_vivre: int):
    """
    Renvoie le nombre de votes d'un livre
    :param id_vivre:
    :return:
    """
    dao_tote = VoteDAO()
    vote_dict = dao_tote.get_voting_results_for(2)

    return vote_dict.count({"id_livre": id_vivre})
