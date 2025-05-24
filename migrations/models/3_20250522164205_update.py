from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caretaker" ALTER COLUMN "phone_number" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caretaker" ALTER COLUMN "phone_number" SET NOT NULL;"""
