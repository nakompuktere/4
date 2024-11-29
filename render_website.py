import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import os
import argparse


def on_reload():
    parser = argparse.ArgumentParser(
        description="создает сайт с книгами"
    )   
    parser.add_argument("--file_path", help="введите путь до файла с данными о книгах", default="library/books_description.json")
    args = parser.parse_args()

    books_per_page_number = 10
    columns_number = 2
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")

    with open(args.file_path, "r", encoding="utf8") as my_file:
        books = json.load(my_file)

    book_pages = list(chunked(books, books_per_page_number))
    pages = len(book_pages)
    for id, book_page in enumerate(book_pages, 1):
        chunked_books = list(chunked(book_page, columns_number))
        
        rendered_page = template.render(
            books=chunked_books,
            current_page=id,
            pages=pages
        )

        with open(f"pages/index{id}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)

def main():
    os.makedirs("pages", exist_ok=True)

    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()