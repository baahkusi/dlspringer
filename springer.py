import os
import time
import requests
import json


def main():

    with open('data/books.json', 'r') as data:
        table = json.load(data)

    try:
        os.mkdir('books')
    except Exception:
        pass

    l = len(table)

    for r, row in enumerate(table):

        dlink = f'https://link.springer.com/content/pdf/10.1007/{row["isbn"]}.pdf'

        print(f'Downloading book {r}/{l} with title, {row["title"]}, from {dlink} ...')

        start = time.time()

        try:
            content = requests.get(dlink).content
        except Exception as e:
            print(f'Download failed. Error - {repr(e)}')
            continue

        with open(f'books/{row["title"]}.pdf', 'wb') as book:
            book.write(content)

        end = time.time()

        duration = end - start

        print(f'Download took {duration} seconds. Size downloaded {len(content)/1000000} MB ...')


main()
