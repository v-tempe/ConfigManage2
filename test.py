import unittest
from hometask2 import generate_plantuml


class MyTestCase(unittest.TestCase):
    def test_click(self):
        expected = "@startuml\nobject click\n\n@enduml\n"
        package_name = "click"
        actual = generate_plantuml(package_name)
        self.assertEqual(actual, expected)

    def test_flask(self):
        expected = "@startuml\nobject flask\nobject Werkzeug\nobject Jinja2\nobject MarkupSafe\nobject Babel\nobject pytz\nobject itsdangerous\nobject click\n\nflask --|> Werkzeug : 0.15\nflask --|> Jinja2 : 2.10.1\nJinja2 --|> MarkupSafe : 0.23\nJinja2 --|> Babel : 0.8\nBabel --|> pytz : 2015.7\nflask --|> itsdangerous : 0.24\nflask --|> click : 5.1\n@enduml\n"
        package_name = "flask"
        with open("output_file.txt") as my_file:
            actual = my_file.read()
        #print(actual)
        #print(expected)
        self.assertEqual(actual, expected)

    def test_none(self):  # тестируем несуществующий пакет
        expected = ""
        package_name = "nothing"
        actual = generate_plantuml(package_name)
        #print(actual)
        #print(expected)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
