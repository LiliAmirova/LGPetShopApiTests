import allure
import jsonschema
import requests
from .schemas.store_order_schema import STORE_ORDER_SCHEMA  # точка обоначает уровень, где находится папка
from .schemas.store_inventory_schema import STORE_INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"
#BASE_URL = "http://rv-school.ru:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Оформление нового заказа в магазине")
    def test_post_new_order_store(self):
        with allure.step("Подготовка данных для оформления заказа "):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на оформление запроса"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), STORE_ORDER_SCHEMA)  # 'это то что пришло к нам в ответе и валидируем с store_schema

        with allure.step("Проверка данных заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity заказа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    def test_get_order_by_id(self, create_order_store):  # тесты с использованием фикстуры
        with allure.step("Получение ID заказа"):
            order_id = create_order_store["id"]
            pet_id = create_order_store["petId"]
            quantity_id =create_order_store["quantity"]
            status_id = create_order_store["status"]
            complete_id = create_order_store["complete"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"
            assert response.json()["id"] == order_id
            assert response.json()["petId"] == pet_id
            assert response.json()["quantity"] == quantity_id
            assert response.json()["status"] == status_id
            assert response.json()["complete"] == complete_id

    @allure.title("Удаление заказа по ID (DELETE/store/order/{orderId}")
    def test_delete_order_by_id(self, create_order_store):  # тесты с использованием фикстуры
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order_store["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа запроса DELETE/store/order/{orderId}"):
            assert response.status_code == 200, f"Код ответа {response.status_code} не совпал с ожидаемым 200"

        with allure.step("Отправка запроса на получение информации об удаленном заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа GET-запроса"):
            assert response.status_code == 404, f"Код ответа {response.status_code} не совпал с ожидаемым 404"

    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId}")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина (GET /store/inventory)")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и формат данных инвентаря"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["approved"]
            assert response.json()["delivered"]
            jsonschema.validate(response.json(), STORE_INVENTORY_SCHEMA)




