from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api")
async def api():
    return {"message": "Hello World"}


app.mount("/media", StaticFiles(directory="media"), name="media")

app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static",
)
