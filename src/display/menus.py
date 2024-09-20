import time

from rich.prompt import Prompt, Confirm

from src.dao.appartient_dao import AppartientDAO
from src.dao.vote_dao import VoteDAO
from src.display.display import DisplayeSelection, DisplayVoteresults, clear_screen
from src.utils.auth import authenticate


def president_menu(id_member: int) -> None:
    """
    Affiche le menu du président
    Ce menu permet d'afficher les résultats des votes pour la deuxième et la troisième sélection
    ainsi que le lauréat.
    Il est possible de quitter.
    """
    dao_appartient: AppartientDAO = AppartientDAO()
    current_round: int = dao_appartient.get_current_round()

    display_votes_results: DisplayVoteresults = DisplayVoteresults(
        "Livres", current_round
    )

    print("[1]. Résultats de votes pour deuxième sélection")
    print("[2]. Résultats de votes pour troisième sélection")
    print("[3]. lauréat")
    print("[4]. Effectuer le prochain vote")
    print("[Q]. Quitter")

    response: str = Prompt.ask(
        "\n Que souhaitez-vous faire? : ", choices=["1", "2", "3", "4", "Q"]
    )

    match response.upper():
        case "Q":
            exit(0)
        case "1":
            handle_round_votes(2, 8)

        case "2":
            handle_round_votes(3, 4)
            president_menu(id_member)
        case "4":
            do_next_vote(current_round, display_votes_results, id_member)
            president_menu(id_member)


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
    Affiche le menu du jury
    Ce menu permet d'effectuer le prochain vote
    Il est possible de quitter
    :param id_member: L'identifiant unique du membre du jury
    """

    dao_appartient: AppartientDAO = AppartientDAO()
    current_round: int = dao_appartient.get_current_round()

    display_votes_results: DisplayVoteresults = DisplayVoteresults(
        "Livres", current_round
    )

    print("[1]. Effectuer le prochain vote")
    print("[Q]. Quitter")

    response: str = Prompt.ask("\nQue souhaitez-vous faire? : ", choices=["1", "Q"])
    while True:
        match response.upper():
            case "Q":
                exit(0)
            case "1":
                do_next_vote(current_round, display_votes_results, id_member)
                menu_commun()


def do_next_vote(current_round, display_votes_results, id_member):
    """
    Permet d'effectuer le prochain vote.
    Si le membre n'a pas encore voté pour la selection en cours, il est invité à choisir 8 livres
    parmi la liste des livres de la sélection actuelle, dans l'ordre décroissant de préference.
    Les votes sont enregistrés dans la base de données.
    :param current_round: L'identifiant de la ronde de vote actuelle.
    :param display_votes_results: L'objet qui permet d'afficher les résultats des votes.
    :param id_member: L'identifiant unique du membre du jury.
    :return: None
    """
    dao_vote: VoteDAO = VoteDAO()

    if dao_vote.has_voted_and_next_round_exists(id_member, current_round) is False:
        display_votes_results.display_whith_id()
        member_choices: list[int] = list_maker(
            "\n Veuillez choisir 8 livres parmi la liste ci-dessus, dans l'ordre décroiant de "
            "préference:"
        )

        dao_vote.send_all_votes_to_db(member_choices, id_member, current_round)

        # menu_jury(id_member)
    else:
        print("\nVous avez déjà voté pour la selection en cours.\n")


def show_welcome_message():
    """
    Fonction qui s'occupe de saluer l'utilisateur en fonction de son role.
    Si l'utilisateur est authentifie, il est salue par son nom ou son titre.
    Sinon, il est informe que l'authentification a echouee.
    :return:
    """
    auth_response: dict = authenticate()

    if auth_response and auth_response["role"] == "Président":
        clear_screen()
        print("\nBonjour Président\n")
        president_menu(auth_response["id_membre"])
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

    :param round_vote: L'identifiant de la ronde de vote
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


def list_maker(message: str) -> list[int]:
    """Crée une liste d'identifiants de livres à partir d'une entrée utilisateur.

    Cette méthode demande à l'utilisateur d'entrer un identifiant pour la
    'Première Liste'. Elle gère plusieurs séparateurs possibles entre les
    identifiants (espaces, tirets ou virgules)."""

    separators = {" ", "-", ","}
    liste = input(message)
    premiere_liste = []

    for separator in separators:
        if separator in liste:
            try:
                premiere_liste = [int(x.strip()) for x in liste.split(separator)]
                break
            except ValueError as e:
                print(
                    f"{e}\nLes separateurs doivent être des espaces, tirets ou virgules)"
                )

    return premiere_liste
