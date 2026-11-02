from pydantic import BaseModel, Field

class Order(BaseModel):
    id: int
    customer: str
    amount: float = Field(gt=0)

o = Order(id=42, customer="Raghu", amount=99.5)
print(o.model_dump())             # dict
print(o.model_dump_json())        # JSON string
print(o.model_dump_json(indent=2))

o2 = Order.model_validate_json('{"id": 7, "customer": "Asha", "amount": "10"}')
print(o2)