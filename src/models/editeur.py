class Editeur:
    """
    Classe qui represente un editeur
    """

    editor_list: list = []

    def __init__(self, nom: str):
        self.id = None
        self.nom = nom

        Editeur.editor_list.append(self)
