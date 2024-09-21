#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.display.menus import menu_commun
from src.utils.factories import initialize_database_in_threads


def main():

    # Initialise la base de données en utilisant des threads.
    initialize_database_in_threads()
    # Affiche le menu commun
    menu_commun()


if __name__ == "__main__":
    main()
