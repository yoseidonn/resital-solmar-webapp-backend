from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "caretaker" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "phone_number" VARCHAR(50) NOT NULL,
    "villa_assignments" JSONB
);
CREATE TABLE IF NOT EXISTS "villa" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "villa_name" VARCHAR(255) NOT NULL,
    "care_taker_id" INT NOT NULL REFERENCES "caretaker" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "resortreportfile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "date" DATE NOT NULL,
    "uploaded_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "apisreportfile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "date" DATE NOT NULL,
    "uploaded_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "resortreport" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "accomodation_name" VARCHAR(255) NOT NULL,
    "supplier" VARCHAR(255) NOT NULL,
    "resort" VARCHAR(255) NOT NULL,
    "opportunity_name" INT NOT NULL,
    "lead_passenger" VARCHAR(255) NOT NULL,
    "holiday_start_date" DATE NOT NULL,
    "holiday_end_date" DATE NOT NULL,
    "total_number_of_passenger" INT NOT NULL,
    "adults" INT NOT NULL,
    "children" INT NOT NULL,
    "infants" INT NOT NULL,
    "flight_arrival_date" DATE NOT NULL,
    "flight_arrival_time" TIMESTAMPTZ NOT NULL,
    "depature_date" DATE NOT NULL,
    "departure_flight_time" TIMESTAMPTZ NOT NULL,
    "extras_aggregated" TEXT NOT NULL,
    "villa_manager_visit_request" VARCHAR(255) NOT NULL,
    "live_villa_manager" VARCHAR(255) NOT NULL,
    "dt_aff_nane" VARCHAR(255) NOT NULL,
    "resort_report_notes" TEXT NOT NULL,
    "resort_report_file_id" INT REFERENCES "resortreportfile" ("id") ON DELETE CASCADE,
    "villa_id_id" INT REFERENCES "villa" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "advancedpassengerinformation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "account_name" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "passenger_name" VARCHAR(255) NOT NULL,
    "opportunity_name" INT NOT NULL,
    "accomodation_name" VARCHAR(255) NOT NULL,
    "holiday_start_date" DATE NOT NULL,
    "holiday_end_date" DATE NOT NULL,
    "age" INT NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "country_of_issue" VARCHAR(255) NOT NULL,
    "document_type" VARCHAR(255) NOT NULL,
    "foid_number" VARCHAR(255) NOT NULL,
    "foid_issue" TIMESTAMPTZ NOT NULL,
    "foid_expiry" TIMESTAMPTZ NOT NULL,
    "nationality" VARCHAR(255) NOT NULL,
    "apis_report_file_id" INT REFERENCES "apisreportfile" ("id") ON DELETE CASCADE,
    "villa_id_id" INT REFERENCES "villa" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "caretakerextrasviewoutput" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fileName" VARCHAR(255) NOT NULL,
    "generatedDate" TIMESTAMPTZ NOT NULL,
    "messages" JSONB,
    "rows" JSONB,
    "content" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "resort_report_file_id" INT NOT NULL REFERENCES "resortreportfile" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "extrasfilteredreservationoutput" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file_name" VARCHAR(255) NOT NULL,
    "generated_date" TIMESTAMPTZ NOT NULL,
    "applied_filters" JSONB,
    "grouped_reservations" JSONB,
    "file_path" VARCHAR(512),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "resort_report_file_id" INT NOT NULL REFERENCES "resortreportfile" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "apisreportoutput" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fileName" VARCHAR(255) NOT NULL,
    "generatedDate" TIMESTAMPTZ NOT NULL,
    "villa" VARCHAR(255),
    "date" VARCHAR(32),
    "rows" JSONB,
    "messages" JSONB,
    "file_path" VARCHAR(512) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "apis_report_file_id" INT NOT NULL REFERENCES "apisreportfile" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
