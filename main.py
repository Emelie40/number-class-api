from fastapi import FastAPI, Query
import requests

app = FastAPI()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return n == sum(d ** power for d in digits)

def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    if response.status_code == 200:
        return response.json().get("text", "No fact available.")
    return "No fact available."

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    num = abs(number)
    properties = ["odd" if num % 2 else "even"]
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    return {
        "number": number,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": get_fun_fact(num)
    }
from fastapi import HTTPException

@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        num = int(number)
    except ValueError:
        response = {
                "number": number,
                "error": True
            }
            # raise HTTPException(status_code=400, detail = response)
            return JSONResponse(status_code=400, content=response)
    properties = ["odd" if num % 2 else "even"]
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": get_fun_fact(num)
    }
