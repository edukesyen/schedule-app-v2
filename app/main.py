from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta

app = FastAPI()

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_leap_years(start_date: datetime, end_date: datetime):
    leap_years = []
    for year in range(start_date.year, end_date.year + 1):
        if is_leap_year(year):
            leap_years.append(f"{year}")
    return leap_years

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Identify Leap Years</title>
            <script>
                async function submitForm(event) {
                    event.preventDefault();
                    const start_date = document.getElementById('start_date').value;
                    const end_date = document.getElementById('end_date').value;

                    const response = await fetch("/submit", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        body: `start_date=${start_date}&end_date=${end_date}`,
                    });

                    const result = await response.text();
                    document.getElementById('result').innerHTML = result;
                }
            </script>
        </head>
        <body>
            <h1>Identify Leap Years</h1>
            <form onsubmit="submitForm(event)">
                <label for="start_date">Start Date:</label>
                <input type="date" id="start_date" name="start_date" required><br><br>
                <label for="end_date">End Date:</label>
                <input type="date" id="end_date" name="end_date" required><br><br>
                <button type="submit">Submit</button>
            </form>
            <div id="result"></div>
        </body>
    </html>
    """

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(start_date: str = Form(...), end_date: str = Form(...)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    leap_years = get_leap_years(start_date, end_date)
    return "<br>".join(leap_years)
