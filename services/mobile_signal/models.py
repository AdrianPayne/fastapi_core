from core.models import ModelBase, ModelRecord


class MobileSignalRecord(ModelRecord, table=True):
    pass


class MobileSignal(ModelBase, table=True):
    _record_model = MobileSignalRecord

    address: str
    latitude: float
    longitude: float
    rssi: float
