PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                }
            },
            "required": ["id", "name"],  # валидация на наличие обязательный полей
            "additionalProperties": False  # обозначаем, что других параметров больше быть не может
        },
        "photoUrls": {
            "type": "array",
            "items": {  # схема для элементов массива
                "type": "string"
            }
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["id", "name"],  # валидация на наличие обязательный полей
                "additionalProperties": False  # обозначаем, что других параметров больше
            }
        },
        "status": {  # это enam
            "type": "string",
            "enam": ["available", "pending", "sold"]  # спислк допустимых значений
        }
    },
    "required": ["id", "name", "photoUrls", "status"],
    "additionalProperties": False
}
