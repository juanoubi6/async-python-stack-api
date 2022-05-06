from databases import Database
from databases.core import Transaction

from .exceptions import TransactionAlreadyStartedException


class BaseTransactionalDAO:
    def __init__(self, db: Database, tx: Transaction = None):
        self.db = db
        self.tx = tx

    async def start_tx(self):
        if self.tx is not None:
            raise TransactionAlreadyStartedException("Transaction already started")

        self.tx = await self.db.transaction()

    async def commit_tx(self):
        if self.tx is None:
            return

        await self.tx.commit()
        self.tx = None

    async def rollback_tx(self):
        if self.tx is None:
            return

        await self.tx.rollback()
        self.tx = None
