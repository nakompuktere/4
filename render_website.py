import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

def main():
    with open("books_description.json", "r", encoding="utf8") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)

    rendered_page = template.render(
        books_parameters=books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

main()

server = Server()

server.watch('template.html', main())

server.serve(root='.')

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()