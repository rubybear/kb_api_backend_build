import uvicorn

from kbb.core.config import settings


def run_dev_server() -> None:
    uvicorn.run("kbb.app.user.app:app" if settings.DEBUG else "0.0.0.0",
                port=8000,
                reload=settings.DEBUG)


if __name__ == "__main__":
    run_dev_server()
