#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.display.display import clear_screen
from src.display.menus import menu_commun
from src.utils.factories import initialize_database_in_threads


def main():
    """
    Fonction principale du programme.

    Initialise la base de données en utilisant des threads, puis affiche le menu commun.
    """
    initialize_database_in_threads()
    clear_screen()
    menu_commun()


if __name__ == "__main__":
    main()
