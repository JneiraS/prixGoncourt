#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from abc import ABC, abstractmethod

from src.dao.auteurs_dao import AuteursDAO
from src.dao.editeurs_dao import EditeursDAO
from src.dao.livres_dao import LivresDAO
from src.dao.membre_jury_dao import MembresJuryDAO
from src.models.auteur import Auteur
from src.models.editeur import Editeur
from src.models.livre import Livre
from src.models.membre_jury import MembreJury

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

    def factory_method(self, information_source: dict) -> Livre:
        """
        Methode qui retourne un nouvel objet Person.
        :param information_source:
        """
        livre: Livre = Livre(
            information_source["titre"],
            information_source["resume"],
            information_source["date_parution"],
            information_source["nombre_pages"],
            information_source["ISBN"],
            information_source["prix"],
        )

        livre.id = information_source["id_livre"]

        return livre


class AuteursCreator(Creator):

    def factory_method(self, information_source: dict) -> Auteur:
        """
        Methode qui retourne un nouvel objet Auteur.
        :param information_source:
        """
        auteur: Auteur = Auteur(
            information_source["nom"],
            information_source["biographie"],
        )

        auteur.id = information_source["id_auteur"]

        return auteur


class EditeursCreator(Creator):

    def factory_method(self, information_source: dict) -> Editeur:
        """
        Methode qui retourne un nouvel objet Editeur.
        :param information_source:
        """
        editeur: Editeur = Editeur(
            information_source["nom"],
        )

        editeur.id = information_source["id_editeur"]

        return editeur


class MembreJuryCreator(Creator):

    def factory_method(self, information_source: dict) -> MembreJury:
        """
        Methode qui retourne un nouvel objet MembreJury.
        :param information_source:
        """
        membre_jury: MembreJury = MembreJury(
            information_source["nom"],
            information_source["role"],
        )

        membre_jury.id = information_source["id_membre"]

        return membre_jury


class MembreJuryDAO:
    pass


def create_all_membre_jury_from_database() -> list[MembreJury]:
    """
    Creer tous les membres du jury de la base de données.
    :return: list[MembreJury]
    """
    membre_jury = MembresJuryDAO()
    results: list[dict] = membre_jury.get_all()
    return list(map(MembreJuryCreator().factory_method, results))


def create_all_editeurs_from_database() -> list[Editeur]:
    """
    Creer tous les editeurs de la base de données.
    :return: list[Editeurs]
    """
    editeurs = EditeursDAO()
    results: list[dict] = editeurs.get_all()
    return list(map(EditeursCreator().factory_method, results))


def create_all_livres_from_database() -> list[Livre]:
    """
    Creer tous les livres de la base de données.
    :return: list[Livres]
    """
    livres = LivresDAO()
    results: list[dict] = livres.get_all()
    return list(map(LivresCreator().factory_method, results))


def create_all_auteurs_from_database() -> list[Auteur]:
    """
    Creer tous les auteurs de la base de données.
    :return: list[Auteurs]
    """
    auteurs = AuteursDAO()
    results: list[dict] = auteurs.get_all()
    return list(map(AuteursCreator().factory_method, results))
