from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to Order Service",
        "status": "Application Running"
    }

@app.get("/orders")
def get_orders():
    return {
        "orders": [
            {"id": 1, "name": "Laptop"},
            {"id": 2, "name": "Mobile"}
        ]
    }