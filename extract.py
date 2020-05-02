import json
import PyPDF2
import requests


def main():
    file = open('springer.pdf', 'rb')

    pdf = PyPDF2.PdfFileReader(file)

    # convert pdf to nice list of dictionary with keys ['title', 'isbn']

    table = []

    start_row = 1

    rows = extract_rows(pdf.getPage(0), start_row, init=True)

    table.extend(rows)

    start_row += len(rows)

    for page in pdf.pages[1:]:

        rows = extract_rows(page, start_row)
        table.extend(rows)

        start_row += len(rows)

    with open('books.json', 'w') as dfile:
        json.dump(table, dfile)


def extract_rows(page, start_row, init=False):

    page_table = page.extractText().split('\n')

    rows = []

    if init:
        page_table = page_table[5:]

    while '' in page_table:
        page_table.remove('')

    end_of_page = False
    while not end_of_page:

        start = page_table.index(str(start_row))

        try:
            end = page_table.index(str(start_row+1))
            row = page_table[start:end]
        except Exception:
            row = page_table[start:]
            end_of_page = True

        url = ''
        for el in row:
            if 'http://' in el:
                url = el

        try:
            print(f'Extracting final ISBN from {url.strip()}, row {start_row} ...')
            isbn = requests.get(url.strip()).url.split('%2F')[-1]

            print(f'ISBN is {isbn} ...')
        except Exception as e:
            print(f'Could not get final ISBN. Error - {repr(e)} ...')
            rows.append({})
            continue

        rows.append({
            '#': start_row,
            'title': row[1],
            'isbn': isbn,
        })

        start_row += 1

    return rows

main()
