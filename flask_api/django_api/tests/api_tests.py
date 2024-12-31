import pytest
from flask import json
from datetime import datetime, date, time
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from app import app
from django_api.api.models import SciRecord
from django_api.api.serializers import SciRecordSerializer

@pytest.mark.django_db
class TestSciRecordAPI(TestCase):
    """Test suite for the Scientific Records API"""
    
    def setUp(self):
        """Set up test client and sample data before each test"""
        self.client = app.test_client()
        self.sample_record = {
            "date": "2024-01-01",
            "time": "12:00:00",
            "time_offset": -5,
            "coordinate": [40.7128, -74.0060],
            "air_temperature": 20.5,
            "humidity": 65.0,
            "wind_speed": 10.2,
            "wind_direction": 180.0,
            "precipitation": 0.0,
            "haze": 5.0,
            "water_temperature": 18.5,
            "notes": "Test record"
        }
        
        # Create a test record in the database
        self.test_record = SciRecord.objects.create(
            date=date(2024, 1, 1),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=20.5,
            humidity=65.0,
            wind_speed=10.2,
            wind_direction=180.0,
            precipitation=0.0,
            haze=5.0,
            water_temperature=18.5,
            notes="Initial test record"
        )
    
    def tearDown(self):
        """Clean up after each test"""
        SciRecord.objects.all().delete()

    def test_create_record(self):
        """Test creating a new record through the API"""
        # Test successful creation
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(self.sample_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        
        # Test duplicate ID prevention
        duplicate_record = self.sample_record.copy()
        duplicate_record['id'] = data['id']
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(duplicate_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid data
        invalid_record = self.sample_record.copy()
        invalid_record['air_temperature'] = "invalid"
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(invalid_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_records(self):
        """Test retrieving all records"""
        # Create additional test records
        SciRecord.objects.create(**self.sample_record)
        
        response = self.client.get('/api/sci_record')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Including the one from setUp

    def test_get_single_record(self):
        """Test retrieving a single record by ID"""
        # Test existing record
        response = self.client.get(f'/api/sci_record/{self.test_record.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], self.test_record.id)
        
        # Test non-existent record
        response = self.client.get('/api/sci_record/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_record(self):
        """Test updating an existing record"""
        update_data = self.sample_record.copy()
        update_data['air_temperature'] = 25.0
        update_data['notes'] = "Updated test record"
        
        # Test successful update
        response = self.client.put(
            f'/api/sci_record/{self.test_record.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['air_temperature'], 25.0)
        self.assertEqual(data['notes'], "Updated test record")
        
        # Test update of non-existent record
        response = self.client.put(
            '/api/sci_record/99999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_record(self):
        """Test deleting a record"""
        # Test successful deletion
        response = self.client.delete(f'/api/sci_record/{self.test_record.id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify record is deleted
        with self.assertRaises(ObjectDoesNotExist):
            SciRecord.objects.get(id=self.test_record.id)
        
        # Test deleting non-existent record
        response = self.client.delete('/api/sci_record/99999')
        self.assertEqual(response.status_code, 404)

    def test_delete_all_records(self):
        """Test deleting all records"""
        # Create additional records
        SciRecord.objects.create(**self.sample_record)
        SciRecord.objects.create(**self.sample_record)
        
        # Verify we have multiple records
        self.assertTrue(SciRecord.objects.count() > 0)
        
        # Delete all records
        response = self.client.delete('/api/sci_record')
        self.assertEqual(response.status_code, 200)
        
        # Verify all records are deleted
        self.assertEqual(SciRecord.objects.count(), 0)

    def test_data_validation(self):
        """Test various data validation scenarios"""
        # Test missing required fields
        invalid_record = {
            "date": "2024-01-01",
            "time": "12:00:00"
            # Missing other required fields
        }
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(invalid_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid data types
        invalid_record = self.sample_record.copy()
        invalid_record['coordinate'] = "not-an-array"
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(invalid_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid date format
        invalid_record = self.sample_record.copy()
        invalid_record['date'] = "01-01-2024"  # Wrong format
        response = self.client.post(
            '/api/sci_record',
            data=json.dumps(invalid_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

class TestSciRecordModel(TestCase):
    """Test suite for the SciRecord Django model"""
    
    def test_model_creation(self):
        """Test creating a SciRecord model instance"""
        record = SciRecord.objects.create(
            date=date(2024, 1, 1),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=20.5,
            humidity=65.0,
            wind_speed=10.2,
            wind_direction=180.0,
            precipitation=0.0,
            haze=5.0,
            water_temperature=18.5,
            notes="Test model creation"
        )
        self.assertIsInstance(record, SciRecord)
        self.assertEqual(str(record), f"Record {record.id}")

class TestSciRecordSerializer(TestCase):
    """Test suite for the SciRecord serializer"""
    
    def test_serialization(self):
        """Test serializing a SciRecord instance"""
        record = SciRecord.objects.create(
            date=date(2024, 1, 1),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=20.5,
            humidity=65.0,
            wind_speed=10.2,
            wind_direction=180.0,
            precipitation=0.0,
            haze=5.0,
            water_temperature=18.5,
            notes="Test serialization"
        )
        
        serializer = SciRecordSerializer(record)
        data = serializer.data
        
        self.assertEqual(data['date'], '2024-01-01')
        self.assertEqual(data['time'], '12:00:00')
        self.assertEqual(data['coordinate'], [40.7128, -74.0060])

    def test_deserialization(self):
        """Test deserializing data to create a SciRecord instance"""
        data = {
            "date": "2024-01-01",
            "time": "12:00:00",
            "time_offset": -5,
            "coordinate": [40.7128, -74.0060],
            "air_temperature": 20.5,
            "humidity": 65.0,
            "wind_speed": 10.2,
            "wind_direction": 180.0,
            "precipitation": 0.0,
            "haze": 5.0,
            "water_temperature": 18.5,
            "notes": "Test deserialization"
        }
        
        serializer = SciRecordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        record = serializer.save()
        self.assertIsInstance(record, SciRecord)
        self.assertEqual(record.air_temperature, 20.5)

if __name__ == '__main__':
    pytest.main()
