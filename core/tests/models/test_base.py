from unittest import TestCase

from ...models.base import ModelBase
from ...models.record import ModelRecord
from ...db.connection import DbSession


# TEST MODELS
class RecordTest(ModelRecord, table=True):
    pass


class Owner:
    def __init__(self, id: int):
        self.id: int = id


class ModelTest(ModelBase, table=True):
    _record_model = RecordTest

    field_a: str
    field_b: int
    field_c: bool


class TestModelBase(TestCase):
    def setUp(self):
        DbSession.create_tables()
        self.owner = Owner(id=1)
        self.create_fields = {"field_a": "test string", "field_b": 10, "field_c": True}

    def tearDown(self):
        ModelTest.delete_table(ModelTest)
        RecordTest.delete_table(RecordTest)

    def test_create_success(self):
        # Given
        create_fields = self.create_fields

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)

        # Then
        self.assertIsInstance(new_item, ModelTest)

    def test_update_success(self):
        # Given
        create_fields = self.create_fields

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        new_item.update({'field_b': 5}, self.owner)

        # Then
        self.assertEqual(5, new_item.field_b)

    def test_delete_success(self):
        # Given
        create_fields = {"field_a": "test string", "field_b": 10, "field_c": True}

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        new_item.delete(self.owner)

        # Then
        self.assertTrue(new_item.deleted)

    def test_create_previous_deleted(self):
        # Given
        create_fields = {"field_a": "test string", "field_b": 10, "field_c": True}

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        new_item.delete(self.owner)

        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)

        # Then
        self.assertIsInstance(new_item, ModelTest)
        self.assertFalse(new_item.deleted)

    def test_get_one_success(self):
        # Given
        create_fields = self.create_fields

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        item_db = ModelTest.get_one(ModelTest, value=new_item.id)

        # Then
        self.assertIsInstance(item_db, ModelTest)
        self.assertEqual(new_item, item_db)

    def test_get_all_success(self):
        # Given
        create_fields = self.create_fields

        # When
        for i in range(3):
            new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        new_item.delete(self.owner)  # Remove the last one
        item_list = ModelTest.get_all(ModelTest)

        # Then
        self.assertIsInstance(item_list[0], ModelTest)
        self.assertEqual(2, len(item_list))  # Excluding deleted one
        self.assertGreater(item_list[-1].id, item_list[0].id)  # Testing order_by
        self.assertEqual(1, item_list[0].id)  # Testing offset
        self.assertLess(len(item_list), 100)  # Testing limit

    def test_update_fail(self):
        """ Try to update with an incorrect value"""
        # Given
        create_fields = self.create_fields

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)

        # Then
        with self.assertRaises(ValueError):
            new_item.update({'field_z': "True"}, self.owner)

    def test_delete_fail(self):
        """ Delete same item twice """
        # Given
        create_fields = {"field_a": "test string", "field_b": 10, "field_c": True}

        # When
        new_item = ModelTest(**create_fields).create(owner_obj=self.owner)
        new_item.delete(self.owner)
        result = new_item.delete(self.owner)

        # Then
        self.assertTrue(new_item.deleted)
        self.assertFalse(result[0])

    def test_get_one_fail(self):
        # Given
        id = 100

        # When & Then
        with self.assertRaises(Exception):
            ModelTest.get_one(ModelTest, value=id)

    def test_records(self):
        # Given
        records = RecordTest.get_all_by_model_and_id(RecordTest, ModelTest, 1)
        records_owner = RecordTest.get_all_by_owner(RecordTest, Owner, 1)
        # TODO: Finish this. TearsDown is deleting the records...
