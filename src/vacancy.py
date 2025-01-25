from typing import Any

import psycopg2

from config import config


class Vacancy:

    def __init__(self) -> None:
        self.__database_name: str = "vacancy"
        self.__params: dict[str, str] = config()

    @property
    def database_name(self) -> str:
        return self.__database_name

    @property
    def params(self) -> dict[str, str]:
        return self.__params

    def create_database(self) -> None:
        """Метод подключается и создает базу данных."""

        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """Метод который подключается к базе данных и создает таблицы."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE organization (
                    organization_id INTEGER PRIMARY KEY,
                    organization_name VARCHAR,
                    organization_url TEXT,
                    open_vacancies INTEGER
                )
            """
            )

            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_name VARCHAR, 
                    vacancies_id INT NOT NULL,
                    vacancies_url TEXT,
                    salary INTEGER,
                    organization_id INT REFERENCES organization(organization_id)
                )
            """
            )

        conn.commit()
        conn.close()

    def filling_database_tables(self, organizations: Any, vacancy: Any) -> None:
        """Метод подключается к базе данных и заполняет таблицы."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for organization in organizations:
                cur.execute(
                    """
                    INSERT INTO organization (organization_id, organization_name, organization_url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    RETURNING organization_id
                    """,
                    (organization["id"], organization["name"], organization["url"], organization["open_vacancies"]),
                )

                for i in vacancy:
                    if i["employer"] == organization["id"]:
                        cur.execute(
                            """
                            INSERT INTO vacancies (organization_id, vacancy_name, vacancies_id, vacancies_url, salary)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (i["employer"], i["name"], i["id"], i["link"], i["salary"]),
                        )

        conn.commit()
        conn.close()
