#!/usr/bin/env python
import uvicorn

with open("index.html", "rb") as file:
    homepage = file.read()


async def echo_server(scope, receive, send):
    """
    ASGI-style 'Hello, world' application.
    """
    if scope["type"] == "http":
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/html"],],
            }
        )
        await send({"type": "http.response.body", "body": homepage})
    elif scope["type"] == "websocket":
        while True:
            event = await receive()

            if event["type"] == "websocket.connect":
                await send({"type": "websocket.accept"})
            elif event["type"] == "websocket.receive":
                await send({"type": "websocket.send", "text": event["text"]})
            elif event["type"] == "websocket.disconnect":
                break


if __name__ == "__main__":
    uvicorn.run(
        "app:echo_server", host="127.0.0.1", port=8000, log_level="info"
    )
