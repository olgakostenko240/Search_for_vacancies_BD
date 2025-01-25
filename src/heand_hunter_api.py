from typing import Any

import requests


class HandHunterAPI:

    def __init__(self) -> None:
        self.__url: str = "https://api.hh.ru/employers"
        self.__params: dict[str, str] = {"sort_by": "by_vacancies_open"}
        self.__name_ids: list[str] = [
            "78638",  # Т-Банк
            "3036416",  # Департамент Ф53
            "2748",  # Ростелеком
            "2180",  # Ozon
            "3529",  # СБЕР
            "9498112",  # Яндекс Крауд
            "1648566",  # Российский Промышленный Сервис
            "4716984",  # X5 Digital
            "4181",  # Банк ВТБ (ПАО)
            "23427",  # Российские железные дороги
        ]

    def get_organization_response(self) -> Any:
        """Метод подключения к API hh.ru"""
        response = requests.get(self.__url, params=self.__params)
        if response.status_code == 200:
            return response
        else:
            return "Ошибка получения данных!"

    def get_organization(self) -> list:
        """Метод для получения не менее 10 компаний"""
        name_organization = []
        response = self.get_organization_response()
        organizations = response.json()["items"]
        for name_id in self.__name_ids:
            for organization in organizations:
                if organization["id"] != name_id:
                    continue
                else:
                    name_organization.append(organization)
        return name_organization

    @staticmethod
    def get_vacancies_response(employers: Any) -> list:
        """Метод для получения вакансий для каждой организации"""
        vacancy = []
        for employer in employers:
            response = requests.get(employer["vacancies_url"], params={"per_page": 100})
            if response.status_code == 200:
                vacancies = response.json()["items"]
                vacancy.extend(vacancies)
        return vacancy

    @staticmethod
    def filter_vacancies(vacancies: Any) -> list[dict[str, int]]:
        """Метод для получения не обходимой информации, для заполнения таблиц в DB, по каждой вакансии"""
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy["salary"] is None:
                salary = 0
            else:
                salary = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
            filtered_vacancies.append(
                {
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "link": vacancy["alternate_url"],
                    "salary": salary,
                    "employer": vacancy["employer"]["id"],
                }
            )
        return filtered_vacancies
