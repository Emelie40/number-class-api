from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    return n == sum(i for i in range(1, n) if n % i == 0)

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    power = len(digits)
    return abs(n) == sum(d ** power for d in digits)

# Function to get a fun fact from Numbers API
def get_fun_fact(n: float) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{int(n)}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fact available.")
    except requests.RequestException:
        return "No fact available."
    return "No fact available."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: float = Query(..., description="The number to classify")):
    # If the number is a whole number, convert to int
    num = int(number) if number.is_integer() else number

    properties = ["odd" if int(num) % 2 else "even"]
    if is_armstrong(int(num)):  # Only check Armstrong for whole numbers
        properties.insert(0, "armstrong")

    response_data = {
        "number": num,
        "is_prime": is_prime(int(num)),
        "is_perfect": is_perfect(int(num)),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(int(num)))),
        "fun_fact": get_fun_fact(num),
    }

    return JSONResponse(content=response_data, status_code=200)

# Custom error handler for invalid input
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"number": request.query_params.get("number", "unknown"), "error": True}
    )
