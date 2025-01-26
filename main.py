from src.dbmanager import DBManager
from src.heand_hunter_api import HandHunterAPI
from src.vacancy import Vacancy


# Работаем с классом HandHunterAPI
hh = HandHunterAPI()
result_organizations = hh.get_organization()
result_vacancies = hh.get_vacancies_response(result_organizations)
result_dict_vacancies = hh.filter_vacancies(result_vacancies)

# Работаем с классом Vacancy
vac = Vacancy()
vac.create_database()
vac.create_tables()
vac.filling_database_tables(result_organizations, result_dict_vacancies)

# Работаем с классом DBManager
db = DBManager()


def main() -> None:

    print(
        """
        Введите запрос для вывода необходимойй вам информации из базы данных.
        1 - Получает список всех компаний и количество вакансий у каждой компани.
        2 - Получает список всех вакансий с указанием компании, вакансии, зарплаты и ссылки на вакансию.
        3 - Получает среднюю зарплату по вакансиям.
        4 - Получает список всех вакансий, у которых зарплата выше средней.
        5 - Получает список всех вакансий, в названии которых содержатся переданное в метод слово.
        """
    )

    user_input = input()

    if user_input == "1":

        d = db.get_companies_and_vacancies_count()
        m = db.execute_query(d)
        print(m)

    elif user_input == "2":

        t = db.get_all_vacancies()
        tm = db.execute_query(t)
        print(tm)

    elif user_input == "3":

        g = db.get_avg_salary()
        gm = db.execute_query(g)
        print(gm)

    elif user_input == "4":

        f = db.get_vacancies_with_higher_salary()
        fm = db.execute_query(f)
        print(fm)

    elif user_input == "5":

        print(
            """
            Введите дополнительно название професии которые вы хотите получить
            """
        )
        user_word = input()
        a = db.get_vacancies_with_keyword(user_word)
        am = db.execute_query(a)
        print(am)

    else:

        print("Нет данных которые вы хотите получить")


if __name__ == "__main__":
    main()
