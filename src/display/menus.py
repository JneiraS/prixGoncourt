from rich.prompt import Prompt

from src.dao.appartient_dao import get_books_in_selection
from src.display.display import DisplayeSelection, clear_screen
from src.utils.auth import authenticate
from src.utils.factories import initialize_database_in_threads


def president_menu() -> None:
    """
    Affiche le menu du-president
    """
    print("[1]. Résultats de votes pour deuxième sélection")
    # TODO Fonction pour afficher les resultats de votes
    print("[2]. Résultats de votes pour troisième sélection")
    print("[3]. lauréat")


def menu_commun() -> None:
    """
    Affiche le menu commun
    """
    clear_screen()

    print("[1]. Afficher les livres de la première sélection")
    print("[2]. Afficher les livres de la deuxième sélection")
    print("[3]. Afficher les livres de la troisième sélection")
    print("[4]. S'identifier")
    print("[Q]. Quitter")

    # Initialise la base de données en utilisant des threads.
    initialize_database_in_threads()

    response: str = Prompt.ask(": ", choices=["1", "2", "3", "4", "Q"])

    match response.lower():
        case "q":
            exit(0)
        case "1":
            first_selection = DisplayeSelection("Première Liste")
            first_selection.display()

        case "2":
            second_selection_list = get_books_in_selection(2)
            second_selection = DisplayeSelection("Seconde Liste", second_selection_list)
            second_selection.display()
        case "3":
            print("Troisième choix")
        case "4":
            greet_user()


def greet_user():
    """
    Fonction qui s'occupe de saluer l'utilisateur en fonction de son role.
    Si l'utilisateur est authentifie, il est salue par son nom ou son titre.
    Sinon, il est informe que l'authentification a echouee.
    :return:
    """
    auth_response: dict = authenticate()
    if auth_response and auth_response["role"] == "Président":
        clear_screen()
        print("Bonjour Président\n")
        president_menu()
    elif auth_response:
        clear_screen()
        print(f"Bienvenue {auth_response['nom']}")
    else:
        print("Authentification echouée")
