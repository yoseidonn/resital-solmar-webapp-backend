from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caretaker" RENAME COLUMN "villa_assignments" TO "assigned_villas";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caretaker" RENAME COLUMN "assigned_villas" TO "villa_assignments";"""
