from sqlmodel import SQLModel, Field
from datetime import datetime

from .record import ModelRecord
from ..db.connection import DbSession


class NoAuthOwner:
    def __init__(self, id: int):
        self.id: int = id


owner = NoAuthOwner(id=0)


class ModelBase(SQLModel):
    """
    Base generic model for the rest of models
    Include:
    - CRUD methods
    - delete is replaced for a boolean
    - id and created_date
    - modified_date for updating and deleting
    Extra logic:
    - create records for creating, updating and deleting
    - integration with the database

    _record_model = son model of ModelRecord to store the records
    """
    id: int | None = Field(default=None, primary_key=True)
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    deleted: bool = False

    _record_model = ModelRecord

    def create(self, owner_obj: any = owner) -> any:
        """
        TODO: Create documentation
        """
        DbSession().update(item=self)
        self._record_model(model_type=self.__class__.__name__, model_id=self.id,
                           operation=self._record_model.OperationType.create,
                           owner_type=owner_obj.__class__.__name__, owner_id=owner_obj.id)
        return self

    def update(self, update_fields: dict, owner_obj: any = owner) -> any:
        """
        Update an item and return it
        Params:
        - update_fields: a dict where key is field name and values teh value of the field
        - owner: the user who is using the method
        Return:
        - The item updated
        Exceptions:
        - Y: key does not exist
        - Z: value type is not correct
        """
        # TODO: Do not include deleted
        self.modified_date = datetime.now()
        for k, v in update_fields.items():
            setattr(self, k, v)
        DbSession().update(item=self)
        self._record_model(model_type=self.__class__.__name__, model_id=self.id,
                           operation=self._record_model.OperationType.update,
                           owner_type=owner_obj.__class__.__name__, owner_id=owner_obj.id)
        return self

    def delete(self, owner_obj: any = owner) -> (bool, str):
        """
        Mark an item as deleted
        Params:
        - id: item id to be deleted
        Return:
        - (True, "success"): The item could be deleted
        - (False, reason): The item could not be deleted and reason
        """
        if self.deleted:
            return False, f"class={self.__class__.__name__} id={self.id} already deleted"

        self.modified_date = datetime.now()
        self.deleted = True
        DbSession().update(item=self)
        self._record_model(model_type=self.__class__.__name__, model_id=self.id,
                           operation=self._record_model.OperationType.delete,
                           owner_type=owner_obj.__class__.__name__, owner_id=owner_obj.id)
        return True, "success"

    @staticmethod
    def get_all(cls, offset: int = 0, limit: int = 100, order_by: any = None) -> list["ModelBase"]:
        """
        Return a list of items
        Params:
        - cls: XXX
        - offset: the first element to be retrieved (default 0) [optional]
        - limit: the max amount of elements to be retrieved (default 100) [optional]
        - order_by: the field key to order by (default "id") [optional]
        - str_match: the value to be used for searching in any field (default "") [optional]
        Return:
        - List of items
        Exceptions:
        - Y: key in order_by does not exist
        """
        if not order_by:
            order_by = cls.id
        return DbSession().get_all(model=cls, offset=offset, limit=limit, order_by=order_by)

    @staticmethod
    def get_one(cls, value: any, key: any = None) -> any:
        """
        Get one item based in a key/value
        Params:
        - cls: XXX
        - value: the value of the field
        - key: the name of the field (default "id") [optional]
        Exceptions:
        - X: Key does not exist
        - W: Key is not unique
        """
        if not key:
            key = cls.id
        return DbSession().get_one(model=cls, key=key, value=value)

    @staticmethod
    def delete_table(cls):
        DbSession().drop(cls)
