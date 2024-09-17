from datetime import date


class Livre:

    book_list: list = []

    def __init__(
        self,
        title: str,
        summary: str,
        publication_date: date,
        number_of_pages: int,
        isbn: str,
        price: float,
    ):

        self.id = None
        self.title = title
        self.summary = summary
        self.publication_date = publication_date
        self.number_of_pages = number_of_pages
        self.isbn = isbn
        self.price = price

        Livre.book_list.append(self)
