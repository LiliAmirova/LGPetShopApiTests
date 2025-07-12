STORE_INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        }
    },
    "required": ["approved", "delivered"],  # валидация на наличие обязательный полей
    "additionalProperties": False # доп поля разрешены
}