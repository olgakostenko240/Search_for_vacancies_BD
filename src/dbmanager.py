from typing import Any

import psycopg2

from src.vacancy import Vacancy


class DBManager(Vacancy):

    def __init__(self) -> None:
        super().__init__()

    def execute_query(self, query: Any) -> Any:
        """Подключается к базе данных."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_companies_and_vacancies_count() -> str:
        """Получает список всех компаний и количество вакансий у каждой компани."""
        query = """
            SELECT organization.organization_name, COUNT(vacancies.vacancy_name) FROM organization, vacancies
            WHERE organization.organization_id=vacancies.organization_id
            GROUP BY organization.organization_name
            """
        return query

    @staticmethod
    def get_all_vacancies() -> str:
        """Получает список всех вакансий с указанием компании, вакансии, зарплаты и ссылки."""
        query = """
            SELECT organization_name, vacancy_name, salary, vacancies_url FROM organization
            INNER JOIN vacancies ON organization.organization_id=vacancies.organization_id
            """
        return query

    @staticmethod
    def get_avg_salary() -> str:
        """Получает среднюю зарплату по вакансиям."""
        query = """
            SELECT AVG(salary) FROM vacancies
            """
        return query

    @staticmethod
    def get_vacancies_with_higher_salary() -> str:
        """Получает список всех вакансий, у которых зарплата выше средней."""
        query = """
            SELECT vacancy_name, salary FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """
        return query

    @staticmethod
    def get_vacancies_with_keyword(query_word: str) -> str:
        """Получает список всех вакансий, в названии которых содержатся переданное в метод слово."""
        query = f"""
            SELECT * FROM vacancies
            WHERE LOWER(vacancy_name) LIKE '%{query_word.lower()}%'
            """
        return query
