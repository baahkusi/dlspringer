import os
import time
import requests
import json


def main():

    with open('books.json', 'r') as data:
        table = json.load(data)

    try:
        os.mkdir('books')
    except Exception:
        pass

    l = len(table)

    s = len(os.listdir('books'))

    for r, row in enumerate(table[s:]):

        dlink = f'https://link.springer.com/content/pdf/10.1007/{row["isbn"]}.pdf'

        print(f'Downloading book {r+s+1}/{l} with title, {row["title"]}, from {dlink} ...')

        start = time.time()

        try:
            content = requests.get(dlink).content
        except Exception as e:
            print(f'Download failed. Error - {repr(e)}')
            continue

        with open(f'books/{row["title"].replace("/","")}.pdf', 'wb') as book:
            book.write(content)

        end = time.time()

        duration = end - start

        print(f'Download took {duration} seconds. Size downloaded {len(content)/1000000} MB ...')


main()
