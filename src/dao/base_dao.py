#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ce fichier contient la classe DatabaseConnectionManager qui s'occupe d'ouvrir et de fermer les
connexions a la base de donnees. Il contient aussi une classe abstraite SingletonMeta qui permet de
transformer une classe en singleton.
"""

from threading import Lock

import pymysql

from src.utils.database_utils import (
    query_database,
    run_query_with_commit,
    insert_and_get_id,
)
from src.utils.database_utils import read_json


class SingletonMeta(type):
    """
    Permet de transformer une classe en singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnectionManager(metaclass=SingletonMeta):
    """
    Classe qui s'occupe d'ouvrir et de fermer les connexions a la base de  données.
    """

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    def open_connection(self) -> None:
        """Opens a database connection."""
        config = read_json("./config/database_config.json")

        self.conn = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def close_connection(self) -> None:
        """
        Ferme la connexion avec la base de données.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_all(self, limit: int = None, offset: int = None) -> list[dict]:
        """
        Récupère tous les enregistrements de la table de la base de données associée à cette instance de
        DatabaseConnectionManager.
        :param limit: Nombre maximal d'enregistrements à renvoyer. La valeur par défaut est None.
        :param offset: Le nombre d'enregistrements à sauter avant de commencer à renvoyer des enregistrements.
        La valeur par défaut est None.
        :return: list[dict] : Une liste de dictionnaires, où chaque dictionnaire représente un
        enregistrement dans la table de la base de données.
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []

        if limit is not None:
            query += f" LIMIT {limit}"
            params.append(limit)

        if offset is not None:
            query += f" OFFSET {offset}"
            params.append(offset)

        results: list[dict] = query_database(self, query)
        return results

    def create(self, query) -> int | None:
        """
        Crée une nouvelle entité dans la base de données et retourne son identifiant.
        :param query:
        """
        return insert_and_get_id(self, query)

    def read(self, identifier: int = None) -> list[dict] | None:
        """
        Récupère une entité dans la base de données selon son identifiant
        :param identifier:
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = {identifier}"
        return query_database(self, query)

    def update(self, table) -> bool:
        """
        Met à jour une entité dans la base de données.
        :param table:
        """
        pass

    def delete(self, id_to_delete: int) -> bool:
        """
        Supprime une entité dans la base de données, grace à son identifiant.
        :param id_to_delete:
        :return:
        """

        query = f"DELETE FROM {self.table_name} WHERE id = {id_to_delete}"
        if run_query_with_commit(self, query):
            return True
        return False
