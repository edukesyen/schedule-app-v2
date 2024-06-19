from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True

def get_prime_numbers(start_number: int, end_number: int):
    prime_numbers = []
    for num in range(start_number, end_number + 1):
        if is_prime(num):
            prime_numbers.append(str(num))
    return prime_numbers

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Identify Prime Numbers</title>
            <script>
                async function submitForm(event) {
                    event.preventDefault();
                    const start_number = document.getElementById('start_number').value;
                    const end_number = document.getElementById('end_number').value;

                    const response = await fetch("/submit", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        body: `start_number=${start_number}&end_number=${end_number}`,
                    });

                    const result = await response.text();
                    document.getElementById('result').innerHTML = result;
                }
            </script>
        </head>
        <body>
            <h1>Identify Prime Numbers</h1>
            <form onsubmit="submitForm(event)">
                <label for="start_number">Start Number:</label>
                <input type="number" id="start_number" name="start_number" required><br><br>
                <label for="end_number">End Number:</label>
                <input type="number" id="end_number" name="end_number" required><br><br>
                <button type="submit">Submit</button>
            </form>
            <div id="result"></div>
        </body>
    </html> 
    """

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(start_number: str = Form(...), end_number: str = Form(...)):
    start_number = int(start_number)
    end_number = int(end_number)
    prime_numbers = get_prime_numbers(start_number, end_number)
    return "<br>".join(prime_numbers)

