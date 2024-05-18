import click
import json
from pathlib import Path


def add_student(students, full_name, group_number, grades):
    """
    Добавить данные о студенте.
    """
    grades = [float(grade) for grade in grades.split()]
    student = {
        "full_name": full_name,
        "group_number": group_number,
        "grades": grades,
    }
    students.append(student)
    students.sort(key=lambda item: item.get("group_number", ""))


def list_students(students):
    """
    Вывести список студентов.
    """
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 15, "-" * 20)
    click.echo(line)
    click.echo(
        "| {:^30} | {:^15} | {:^20} |".format("Ф.И.О.", "Номер группы", "Успеваемость")
    )
    click.echo(line)
    for student in students:
        average_grade = sum(student.get("grades", 0)) / len(student.get("grades", 1))
        if average_grade > 4.0:
            click.echo(
                "| {:<30} | {:<15} | {:<20} |".format(
                    student.get("full_name", ""),
                    student.get("group_number", ""),
                    ", ".join(map(str, student.get("grades", []))),
                )
            )
    click.echo(line)


def save_to_json(filepath, data):
    """
    Сохранить всех студентов в файл JSON.
    """
    with filepath.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(filepath):
    """
    Загрузить всех студентов из файла JSON.
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
@click.option("-f", "--filename", required=True, help="The data file name")
@click.option("-n", "--name", required=True, help="The student's full name")
@click.option("-g", "--group", required=True, help="The student's group number")
@click.option("-r", "--grades", required=True, help="The student's grades")
def add(filename, name, group, grades):
    """
    Add a new student.
    """
    home_dir = Path.home()
    filepath = home_dir / filename
    students = load_from_json(filepath)
    add_student(students, name, group, grades)
    save_to_json(filepath, students)


@cli.command()
@click.option("-f", "--filename", required=True, help="The data file name")
def display(filename):
    """
    Display all students.
    """
    home_dir = Path.home()
    filepath = home_dir / filename
    students = load_from_json(filepath)
    list_students(students)


if __name__ == "__main__":
    cli()
