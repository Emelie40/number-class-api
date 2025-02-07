from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return n == sum(d ** power for d in digits)

# Function to get a fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fact available.")
    except requests.RequestException:
        return "No fact available."
    return "No fact available."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number = Query(..., description="The number to classify")):
    if isinstance(number, str):
        try:
            number = int(number)
        except ValueError:
            response_data = {
                "number": number,
                "error": True
            }
            return JSONResponse(status_code=400, content=response_data)
    
    num = abs(number)
    properties = ["odd" if num % 2 else "even"]
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    response_data = {
        "number": number,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": get_fun_fact(num),
    }

    return response_data

# # Custom error handler for invalid input
# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request, exc):
#     return {
#         "number": request.query_params.get("number", "unknown"),
#         "error": True
#     }