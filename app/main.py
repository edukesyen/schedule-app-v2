from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta

app = FastAPI()

def get_weekend_dates(start_date: datetime, end_date: datetime):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 5:  # Saturday
            dates.append(current_date.strftime("%A, %d %B %Y"))
        elif current_date.weekday() == 6:  # Sunday
            dates.append(current_date.strftime("%A, %d %B %Y"))
        current_date += timedelta(days=1)
    return dates

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Identify Weekends</title>
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
    </html>
    """


