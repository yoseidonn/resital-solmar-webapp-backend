TORTOISE_ORM = {
    "connections": {
        "default": "postgres://resital_solmar:q-24a2ss@localhost:5432/resital_solmar_webapp"
    },
    "apps": {
        "models": {
            "models": [
                "models.caretaker",
                "models.villa",
                "models.resort_report_file",
                "models.apis_report_file",
                "models.resort_report",
                "models.advanced_passenger_information",
                "models.caretaker_extras_view_output",
                "models.extras_filtered_reservation_output",
                "models.apis_report_output",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}