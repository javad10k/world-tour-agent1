from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="World Tour Agent")

client = OpenAI()


class AgentRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>World Tour Agent</title>
    </head>

    <body>
        <h1>World Tour Agent</h1>

        <textarea id="message"
            rows="6"
            style="width:100%;"
            placeholder="درخواست خودت را بنویس..."></textarea>

        <br><br>

        <button onclick="sendMessage()">ارسال</button>

        <pre id="answer"></pre>

        <script>
            async function sendMessage() {

                const message =
                    document.getElementById("message").value;

                const answer =
                    document.getElementById("answer");

                answer.textContent =
                    "در حال تحقیق...";

                try {

                    const response = await fetch("/agent", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    answer.textContent =
                        data.response || "خطایی رخ داد.";

                } catch (error) {

                    answer.textContent =
                        "ارتباط با Agent برقرار نشد.";

                }
            }
        </script>

    </body>
    </html>
    """


@app.post("/agent")
def run_agent(request: AgentRequest):

    response = client.responses.create(
        model="gpt-5.6-luna",
        tools=[
            {
                "type": "web_search"
            }
        ],
        input=request.message
    )

    return {
        "status": "success",
        "response": response.output_text
    }
