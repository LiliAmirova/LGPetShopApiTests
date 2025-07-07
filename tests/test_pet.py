import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA  # точка обоначает уровень, где находится папка

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца "):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(),PET_SCHEMA)  # 'это то что пришло к нам в ответе и валидируем с pet_schema

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными (POST /pet)")
    def test_add_full_pet(self):
        with allure.step("Подготовка полных данных для создания питомца "):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["https://site.com/bulldog/photo"],
                "tags": [{
                    "id": 0,
                    "name": "#dog"
                }],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца c полными данными "):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"
            jsonschema.validate(response.json(),PET_SCHEMA)  # 'это то что пришло к нам в ответе и валидируем с pet_schema

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], f"id питомца: {response_json['id']} не совпадает с ожидаемым: {payload['id']}"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['category']['id'] == payload['category']['id'], "category.id питомца не совпадает с ожидаемым"
            assert response_json['category']['name'] == payload['category']['name'], "category.name питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'][0]['id'] == payload['tags'][0]['id'], "tags.id питомца не совпадает с ожидаемым"
            assert response_json['tags'][0]['name'] == payload['tags'][0]['name'], "tags.name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):  # тесты с использованием фикстуры
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце (PUT/pet)")
    def test_update_pet_by_id(self, create_pet): # тесты с использованием фикстуры
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"

        with allure.step("Проверка обновленных данных питомца"):
            assert response_json['id'] == payload['id'], f"id питомца: {response_json['id']} не совпадает с ожидаемым: {payload['id']}"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID (DELETE/pet/{petId}")
    def test_delete_pet_by_id(self, create_pet): # тесты с использованием фикстуры
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа запроса DELETE/pet/{petId}"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"

        with allure.step("Отправка запроса на получение информации об удаленном питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа GET-запроса"):
            assert response.status_code == 404, f"Код ответа {response.status_code} не совпал с ожидаемым 404"


