#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

from src.dao.livres_dao import LivresDAO
from src.models.livres import Livres

"""
Ce fichier contient la classe Creator qui s'occupe de la creation d'objets.
"""


class Creator(ABC):

    @abstractmethod
    def factory_method(self, information_source) -> None:
        """
        Méthode abstraite qui doit être implémentée.
        Cette méthode prend une source d'information en entrée et créer un nouvel objet.
        :param information_source:
        :return:
        """
        pass


class LivresCreator(Creator):

    def factory_method(self, information_source: dict) -> Livres:
        """
        Methode qui retourne un nouvel objet Person.
        :param information_source:
        :return:
        """
        person: Livres = Livres(
            information_source["titre"],
            information_source["resume"],
            information_source["date_parution"],
            information_source["nombre_pages"],
            information_source["ISBN"],
            information_source["prix"],
        )

        person.id = information_source["id_livre"]

        return person


def create_all_livres_from_database() -> list[Livres]:
    """
    Creer tous les livres de la base de données.
    :return: list[Livres]
    """
    livres = LivresDAO()
    results: list[dict] = livres.get_all()
    return list(map(LivresCreator().factory_method, results))
