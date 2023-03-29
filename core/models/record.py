from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field

from ..db.connection import DbSession


class ModelRecord(SQLModel):
    """
    Record model for creating, updating and deleting other models
    """

    class OperationType(Enum):
        create: str = "create"
        update: str = "update"
        delete: str = "delete"

    id: int | None = Field(default=None, primary_key=True)
    created_date: datetime = datetime.now()
    model_type: str
    model_id: int | None
    operation: OperationType
    owner_type: str
    owner_id: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        DbSession().update(self)

    @staticmethod
    def get_all_by_model_and_id(cls, model: any, model_id: int) -> list[any]:
        """
        Return a list of records by model and id
        Params:
            - model_type: type of model affected
            - model_id: id of model affected
        Return:
            - List of records
        Exceptions:
            - A: Model does not exist
            - B: id does not exist
        """
        return DbSession().get_all_records(cls, model_type=model.__class__.__name__, model_id=model_id)

    @staticmethod
    def get_all_by_owner(cls, owner: any, owner_id: int) -> list[any]:
        """
        Return a list of records by owner
        Params:
            - owner_type: type of owner model
            - owner_id: id of owner
        Return:
            - List of records
        Exceptions:
            - A: Model does not exist
            - B: id does not exist
        """
        return DbSession().get_all_records_by_owner(cls, owner_type=owner.__class__.__name__, owner_id=owner_id)

    @staticmethod
    def delete_table(cls):
        DbSession().drop(cls)
