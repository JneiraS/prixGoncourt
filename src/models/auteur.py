class Auteur:
    """
    Classe qui represente un auteur
    """

    auteur_list: list = []

    def __init__(self, nom: str, biographie: str):
        self.id = None
        self.nom = nom
        self.biographie = biographie

        Auteur.auteur_list.append(self)
