import hashlib

from rich.prompt import Prompt

from src.dao.membre_jury_dao import MembresJuryDAO


class Authentication:
    def __init__(self, password: str):
        self.password = password

    def hash_password(self) -> str:
        """
        Retourne le mot de passe haché avec la fonction de hachage SHA-256.
        """
        return hashlib.sha256(self.password.encode()).hexdigest()

    def check_password(self) -> dict:
        """
        Vérifie si le mot de passe enregistré correspond celui donné.
        :return: True si le mot de passe est correct, False sinon.
        """
        dao_membre: MembresJuryDAO = MembresJuryDAO()
        membre_jury_passwords: list[dict] = dao_membre.gethash()

        for password in membre_jury_passwords:
            if password["mot_de_passe"] == self.hash_password():
                return password

    def delete_auth(self):
        """
        Supprime l'objet Authentication.
        """
        del self


def authenticate() -> dict:
    """
    Authentifie un membre du jury.
    """

    password: str = Prompt.ask("Veuillez entrer votre mot de passe: ")
    auth = Authentication(password)
    response = auth.check_password()
    if response:
        del auth
        return response
