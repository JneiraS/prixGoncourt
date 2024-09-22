import unittest
import json
import os
from src.utils.database_utils import read_json


class TestReadJsonFunction(unittest.TestCase):

    def test_valid_json_file(self):
        # Créer un fichier JSON valide
        file_name = "test.json"
        with open(file_name, "w") as file:
            json.dump({"key": "value"}, file)

        result = read_json(file_name)
        self.assertEqual(result, {"key": "value"})
        os.remove(file_name)

    def test_invalid_json_file(self):
        # Créer un fichier JSON invalide
        file_name = "test.json"

        with open(file_name, "w") as file:
            file.write("Invalid JSON")

        with self.assertRaises(json.JSONDecodeError):
            read_json(file_name)
        os.remove(file_name)

    def test_non_existent_file(self):
        # Test la fonction read_json avec un fichier non existant
        with self.assertRaises(FileNotFoundError):
            read_json("non_existent_file.json")

    def test_non_json_file(self):
        # Test la fonction read_json avec un fichier qui n'est pas un JSON
        file_name = "test.txt"
        with open(file_name, "w") as file:
            file.write("This is not a JSON file")

        with self.assertRaises(json.JSONDecodeError):
            read_json(file_name)

        os.remove(file_name)


if __name__ == "__main__":
    unittest.main()
