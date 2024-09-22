import unittest
from datetime import date

from src.models.livre import Livre
from src.models.membre_jury import MembreJury
from src.utils.factories import Creator, MembreJuryCreator, LivresCreator


class TestCreatorFactoryMethod(unittest.TestCase):

    def test_factory_method_is_abstract(self):

        with self.assertRaises(TypeError):
            Creator()

    def setUp(self):
        self.membre_jury = MembreJuryCreator()
        self.livre = LivresCreator()

    def test_factory_method(self):
        information_source_membre_jury = {
            "nom": "John Doe",
            "role": "President",
            "id_membre": "12345",
        }
        information_source_livre = {
            "titre": "Le Seigneur des Anneaux",
            "resume": "Le Seigneur des Anneaux est un roman de fantasy.",
            "date_parution": "2000-01-01",
            "nombre_pages": 1000,
            "ISBN": "1234567890",
            "prix": 9.99,
            "id_livre": "12345",
        }

        membre_jury = self.membre_jury.factory_method(information_source_membre_jury)
        livre = self.livre.factory_method(information_source_livre)

        self.assertIsInstance(livre, Livre)
        self.assertEqual(livre.title, "Le Seigneur des Anneaux")
        self.assertEqual(
            livre.summary, "Le Seigneur des Anneaux est un roman de fantasy."
        )
        self.assertEqual(livre.publication_date, date(2000, 1, 1).strftime("%Y-%m-%d"))
        self.assertEqual(livre.number_of_pages, 1000)
        self.assertEqual(livre.isbn, "1234567890")
        self.assertEqual(livre.price, 9.99)

        self.assertIsInstance(membre_jury, MembreJury)
        self.assertEqual(membre_jury.nom, "John Doe")
        self.assertEqual(membre_jury.role, "President")
        self.assertEqual(membre_jury._id, "12345")


if __name__ == "__main__":
    unittest.main()
