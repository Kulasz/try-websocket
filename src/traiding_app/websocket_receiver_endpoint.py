from fastapi import APIRouter
from fastapi.responses import HTMLResponse

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Receiver</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        #messages {
            list-style-type: none;
            padding: 0;
        }
        #messages li {
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            margin: 5px 0;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>WebSocket Messages</h1>
    <div>
        <ul id="messages"></ul>
    </div>

    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
        };

        ws.onerror = function(error) {
            console.error('WebSocket Error:', error);
        };

        ws.onclose = function() {
            console.log('WebSocket connection closed');
        };
    </script>
</body>
</html>"""

router = APIRouter(prefix="/frontend")


@router.get("/")
async def get():
    return HTMLResponse(HTML)
