import time

from rich.prompt import Prompt, Confirm

from src.dao.appartient_dao import AppartientDAO
from src.dao.vote_dao import VoteDAO
from src.display.display import DisplayeSelection, DisplayVoteresults, clear_screen
from src.utils.auth import authenticate


def president_menu() -> None:
    """
    Affiche le menu du président
    Ce menu permet d'afficher les résultats des votes pour la deuxième et la troisième sélection
    ainsi que le lauréat.
    Il est possible de quitter.
    """
    print("[1]. Résultats de votes pour deuxième sélection")
    print("[2]. Résultats de votes pour troisième sélection")
    print("[3]. lauréat")
    print("[Q]. Quitter")

    response: str = Prompt.ask(
        "\n Que souhaitez-vous faire? : ", choices=["1", "2", "3", "4", "Q"]
    )

    match response.lower():
        case "q":
            exit(0)
        case "1":
            handle_round_votes(2, 8)

        case "2":
            handle_round_votes(3, 4)


def menu_commun() -> None:
    """
    Affiche le menu commun
    Ce menu permet d'afficher les livres de la première, deuxième, troisième liste
    ainsi que le lauréat. Il est possible de s'identifier.

    """

    # clear_screen()

    print("[1]. Afficher les livres de la première sélection")
    print("[2]. Afficher les livres de la deuxième sélection")
    print("[3]. Afficher les livres de la troisième sélection")
    print("[4]. Afficher le lauréat")
    print("[5]. S'identifier")
    print("[Q]. Quitter")

    response: str = Prompt.ask(
        "\n Que souhaitez-vous faire? : ", choices=["1", "2", "3", "4", "5", "Q"]
    )

    while True:
        match response.upper():
            case "Q":
                exit(0)
            case "1":
                first_selection = DisplayeSelection("Première Liste")
                first_selection.display()
                menu_commun()

            case "2":
                doa_appartient = AppartientDAO()
                second_selection_list = doa_appartient.get_books_in_selection(2)
                second_selection = DisplayeSelection(
                    "Seconde Liste", second_selection_list
                )
                second_selection.display()
                menu_commun()

            case "3":
                doa_appartient = AppartientDAO()
                thrird_selection_list = doa_appartient.get_books_in_selection(3)
                thrird_selection = DisplayeSelection(
                    "Troisième Liste", thrird_selection_list
                )
                thrird_selection.display()
                menu_commun()

            case "5":
                show_welcome_message()


def menu_jury(id_member: int):
    """
    Affiche le menu des Jurys
    :return:
    """

    dao_vote = VoteDAO()
    print("[1]. Effectuer le prochain vote")
    print("[Q]. Quitter")

    response: str = Prompt.ask("\nQue souhaitez-vous faire? : ", choices=["1", "Q"])
    while True:
        match response.upper():
            case "Q":
                exit(0)
            case "1":
                if dao_vote.has_voted_and_next_round_exists(id_member, 2) is False:
                    print("Vous pouvez voter!")
                else:
                    print("\nVous avez déjà voté pour la selection en cours.\n")
                menu_commun()


def show_welcome_message():
    """
    Fonction qui s'occupe de saluer l'utilisateur en fonction de son role.
    Si l'utilisateur est authentifie, il est salue par son nom ou son titre.
    Sinon, il est informe que l'authentification a echouee.
    :return:
    """
    auth_response: dict = authenticate()

    if auth_response and auth_response["role"] == "Président\n":
        clear_screen()
        print("Bonjour Président\n")
        president_menu()
    elif auth_response:
        clear_screen()
        print(f"Bienvenue {auth_response['nom']}\n")
        menu_jury(auth_response["id_membre"])
    else:

        print("Authentification echouée")
        time.sleep(3)
        menu_commun()


def handle_round_votes(round_vote: int, books_selected: int):
    """
    Affiche les résultats des votes pour une ronde de vote donnée,
    valide le résultat si demandé, et sauvegarde les livres sélectionnés
    dans la table Appartient.

    :param round_vote: l'identifiant de la ronde de vote
    :param books_selected: le nombre de livres à sélectionner
    :return: None
    """
    doa_vote: VoteDAO = VoteDAO()
    dao_appartient: AppartientDAO = AppartientDAO()

    votes_results = DisplayVoteresults(
        "Resultats des votes pour la sélection", round_vote
    )
    votes_results.display()
    if Confirm.ask("Valider le resultats des votes ?"):
        votes_results_for_round_two: list[dict] | None = (
            doa_vote.get_voting_results_for(round_vote, books_selected)
        )
        # creer une liste avec les identifiants des livres
        list_results_for_round_two = [
            k["id_livre"] for k in votes_results_for_round_two
        ]

        if (
            dao_appartient.add_books_to_selection(
                round_vote, list_results_for_round_two
            )
            is False
        ):
            print("Une erreure est survenue lors de la sauvegarde des votes")
        else:
            print("\nVotes intégrés avec succès\n")
    president_menu()
