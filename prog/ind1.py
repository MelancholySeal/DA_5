import os
import click
import json
from datetime import datetime
from pathlib import Path


def get_home_directory():
    """
    Получить домашний каталог пользователя.
    """
    return Path.home()


def get_filename(filename_option):
    """
    Получить имя файла из переменной окружения, из командной строки или использовать файл в домашнем каталоге.
    """
    filename_env = os.getenv("PEOPLE_FILE")
    if filename_option:
        return Path(filename_option)
    elif filename_env:
        return Path(filename_env)
    else:
        return get_home_directory() / "people.json"


def add_person(people, full_name, birth_date, phone_number):
    """
    Добавить данные о человеке.
    """
    person = {
        "full_name": full_name,
        "birth_date": birth_date,
        "phone_number": phone_number,
    }
    people.append(person)
    people.sort(key=lambda item: datetime.strptime(item["birth_date"], "%Y-%m-%d"))


def list_people(people):
    """
    Вывести список людей.
    """
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 15, "-" * 15)
    click.echo(line)
    click.echo(
        "| {:^30} | {:^15} | {:^15} |".format("Ф.И.О.", "Дата рождения", "Телефон")
    )
    click.echo(line)
    for person in people:
        click.echo(
            "| {:<30} | {:<15} | {:<15} |".format(
                person.get("full_name", ""),
                person.get("birth_date", ""),
                person.get("phone_number", ""),
            )
        )
    click.echo(line)


def find_person_by_phone(people, phone_number):
    """
    Найти человека по номеру телефона.
    """
    for person in people:
        if person.get("phone_number") == phone_number:
            return person
    return None


def save_to_json(filepath, data):
    """
    Сохранить всех людей в файл JSON.
    """
    with filepath.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(filepath):
    """
    Загрузить всех людей из файла JSON.
    """
    try:
        if filepath.exists():
            with filepath.open("r", encoding="utf-8") as file:
                return json.load(file)
        else:
            click.echo(f"Файл {filepath} не существует.")
            return []
    except Exception as e:
        click.echo(
            f"Произошла ошибка при загрузке данных из файла {filepath}: {str(e)}"
        )
        return []


@click.group()
def cli():
    pass


@cli.command()
@click.option("-f", "--filename", help="The data file name")
@click.option("-n", "--name", required=True, help="The person's full name")
@click.option("-b", "--birthdate", required=True, help="The person's birth date (YYYY-MM-DD)")
@click.option("-p", "--phone", required=True, help="The person's phone number")
def add(filename, name, birthdate, phone):
    """
    Add a new person.
    """
    filepath = get_filename(filename)
    people = load_from_json(filepath)
    add_person(people, name, birthdate, phone)
    save_to_json(filepath, people)


@cli.command()
@click.option("-f", "--filename", help="The data file name")
def display(filename):
    """
    Display all people.
    """
    filepath = get_filename(filename)
    people = load_from_json(filepath)
    list_people(people)


@cli.command()
@click.option("-f", "--filename", help="The data file name")
@click.option("-p", "--phone", required=True, help="The person's phone number")
def find(filename, phone):
    """
    Find a person by phone number.
    """
    filepath = get_filename(filename)
    people = load_from_json(filepath)
    person = find_person_by_phone(people, phone)
    if person:
        click.echo(f"Ф.И.О.: {person['full_name']}")
        click.echo(f"Дата рождения: {person['birth_date']}")
        click.echo(f"Телефон: {person['phone_number']}")
    else:
        click.echo(f"Человек с номером телефона {phone} не найден.")


if __name__ == "__main__":
    cli()
