from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routes import (
    caretaker_router,
    villa_router,
    resort_report_file_router,
    resort_report_router,
    apis_report_file_router,
    advanced_passenger_information_router,
    resort_report_output_router,
    apis_report_output_router,
)

app = FastAPI()

app.include_router(caretaker_router)
app.include_router(villa_router)
app.include_router(resort_report_file_router)
app.include_router(resort_report_router)
app.include_router(apis_report_file_router)
app.include_router(advanced_passenger_information_router)
app.include_router(resort_report_output_router)
app.include_router(apis_report_output_router)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"} 