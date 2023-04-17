from sqlmodel import Session, create_engine, SQLModel, select

from config import settings

sqlite_url = settings.database_url
engine = create_engine(sqlite_url)


class DbSession:

    @staticmethod
    def create_tables():
        SQLModel.metadata.create_all(engine)

    def update(self, item: any) -> object:
        """ Create or modify """
        with Session(engine) as session:
            print(item)
            session.add(item)
            session.commit()
            session.refresh(item)
            return item

    def get_one(self, model: any, key: str, value: any) -> object:
        with Session(engine) as session:
            result = session.exec(
                select(model).where((key == value) & (model.deleted == False))
            ).one()
            return result

    def get_all(self, model: any, offset: int, limit: int, order_by: any):
        """ Get all items excluding delete ones """
        with Session(engine) as session:
            result = session.exec(
                select(model).where(model.deleted == False).order_by(order_by).offset(offset).limit(limit)
            ).all()
            return result

    def drop(self, model: any):
        model.__table__.drop(engine)

    def get_all_records(self, cls: any, model_type: any, model_id: int):
        """ Get all records for a model and an ID """
        with Session(engine) as session:
            result = session.exec(select(cls).where(cls.model_id == model_id).order_by(cls.id)).all()
            return result

    def get_all_records_by_owner(self, cls: any, owner_type: any, owner_id: int):
        """ Get all records by an owner """
        with Session(engine) as session:
            result = session.exec(
                select(cls)
                .where(cls.owner_type == owner_type)
                .where(cls.owner_id == owner_id)
                .order_by(cls.id)
            ).all()
            return result

