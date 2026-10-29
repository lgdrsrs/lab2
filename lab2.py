import csv
import random
from xml.dom import minidom


def read_books(filename):
    books = []
    with open(filename, encoding="cp1251") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        for row in reader:
            books.append(row)
    return books


def count_long_titles(books):
    count = 0
    for book in books:
        if len(book[1]) > 30:
            count += 1
    return count


def get_year(book):
    try:
        year = int(book[6].split()[0].split('.')[2])
    except (IndexError, ValueError):
        return None
    return year


def search_by_author(books, author):
    author = author.lower()
    searched_books = []
    for book in books:
        year = get_year(book)
        if year is None:
            continue
        if 2016 <= year <= 2018 and (author in book[3].lower()
                                     or author in book[4].lower()):
            searched_books.append(book)
    return searched_books


def write_references(books, filename):
    defined_books = {}
    for book in books:
        if get_year(book) is not None and book[3] != "":
            key = (book[1], book[3])
            defined_books[key] = book
    books_reference = random.sample(list(defined_books.values()), 20)
    with open(filename, "w", encoding="utf-8") as f:
        for i, book in enumerate(books_reference, start=1):
            year = get_year(book)
            f.write(f"{i}. {book[3]}. {book[1]} - {year}\n")


def get_text(element, tag):
    return element.getElementsByTagName(tag)[0].firstChild.data


def get_char_codes(filename):
    char_codes = []
    dom = minidom.parse(filename)

    valutes = dom.getElementsByTagName("Valute")
    for valute in valutes:
        nominal = int(get_text(valute, "Nominal"))
        if nominal in (10, 100):
            char_codes.append(get_text(valute, "CharCode"))
    return char_codes


def get_unique_tags(books):
    unique_tags = set()
    for book in books:
        tags = book[12].split("#")
        for tag in tags:
            tag = tag.strip()
            if tag:
                unique_tags.add(tag)
    return unique_tags


def get_top_books(books, n=20):
    all_books = {}
    for book in books:
        key = (book[1], book[3])
        all_books[key] = all_books.get(key, 0) + int(book[8])
    return sorted(all_books.items(),
                  key=lambda item: item[1], reverse=True)[:n]


def main():
    books = read_books("books.csv")
    long_titles_qty = count_long_titles(books)
    print("Названий длиннее 30 символов:", long_titles_qty)
    print()

    while True:
        author = input("Автор (Enter - выход): ").strip()
        if not author:
            break
        found_books = search_by_author(books, author)
        if not found_books:
            print("Ничего не найдено")
        for i, book in enumerate(found_books, start=1):
            print(f"{i}. {book[1]} - {book[3]}, {get_year(book)}")
    print()

    char_codes = get_char_codes("currency.xml")
    codes_text = ", ".join(char_codes)
    print(f"Коды валют номиналами 100 или 10 "
          f"({len(char_codes)} шт.): {codes_text}")
    print()

    write_references(books, "references.txt")
    print("Файл с подборкой 20 книг успешно сохранен")
    print()

    unique_tags = list(get_unique_tags(books))
    tags_text = ";\n".join(unique_tags[:10])
    print(f"Различных тегов: {len(unique_tags)}; Первые 10 уникальных тегов:")
    print(f"{tags_text}")
    print("Осталось тегов:", len(unique_tags) - 10)
    print_others = input("Вывести остальные? Y/N ")
    if print_others == "Y":
        print(";\n".join(unique_tags[11:]))
    print()

    top_books = get_top_books(books)
    print("Топ книг по количеству выдач:")
    for i, ((title, author), total) in enumerate(top_books, start=1):
        print(f"{i}. {title} - {author}. Выдач: {total}")


if __name__ == "__main__":
    main()
