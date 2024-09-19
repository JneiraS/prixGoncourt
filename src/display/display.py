import os
import platform
from abc import ABC, abstractmethod

from rich import box
from rich.console import Console
from rich.table import Table

from src.dao.ecrit_dao import EcritDAO
from src.dao.edit_dao import EditDAO
from src.models.livre import Livre


class Display(ABC):

    @abstractmethod
    def display(self):
        """
        Affiche l'interface graphique
        :return:
        """
        pass


class DisplayeSelection(Display):

    def __init__(self, table_title: str, list_of_selected_books=None):

        if list_of_selected_books is None:
            list_of_selected_books = Livre.book_list

        self.table_title = table_title
        self.list_of_selected_books = list_of_selected_books

    def display(self):
        console = Console()
        dao_ecrit = EcritDAO()
        dao_edit = EditDAO()
        terminal_width = console.size.width - 4
        table = Table(
            show_header=True,
            title=f"\n\n\n{self.table_title}",
            box=box.SQUARE,
            width=terminal_width,
            header_style="dodger_blue1",
            border_style="grey42",
        )
        table.add_column(
            "Titres", style="dim", width=6, justify="center", vertical="middle"
        )
        table.add_column(
            "Résumés", style="dim", width=14, justify="center", vertical="middle"
        )
        table.add_column(
            "Auteur", style="dim", width=3, justify="center", vertical="middle"
        )
        table.add_column(
            "Date de publication",
            style="dim",
            width=2,
            justify="center",
            vertical="middle",
        )
        table.add_column(
            "Editeur", style="dim", width=4, justify="center", vertical="middle"
        )
        table.add_column(
            "Nombre de pages", style="dim", width=1, justify="center", vertical="middle"
        )
        table.add_column(
            "ISBN", style="dim", width=3, justify="center", vertical="middle"
        )
        table.add_column(
            "Prix", style="dim", width=1, justify="center", vertical="middle"
        )

        for livre in self.list_of_selected_books:
            table.add_row(
                livre.title,
                livre.summary,
                dao_ecrit.get_auteur_by_livre_id(livre.id),
                str(livre.publication_date),
                dao_edit.get_editeur_name_by_livre_id(livre.id),
                str(livre.number_of_pages),
                livre.isbn,
                str(livre.price) + "€",
            )
            table.add_row("", "", style="grey42", end_section=True)

        clear_screen()
        console.print(table)


def clear_screen() -> None:
    """
    Efface l'écran sur le terminal, en fonction du systeme
    :return:
    """
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")
