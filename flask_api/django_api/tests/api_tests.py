import pytest
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import date, time
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django_api.api.models import SciRecord
from django_api.api.serializers import SciRecordSerializer

class BaseTestCase(TransactionTestCase):
    """Base test class with database setup"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure migrations are applied
        call_command('migrate')

    def setUp(self):
        super().setUp()
        # Reset the database state
        call_command('flush', '--no-input')
        self.client = APIClient()

@pytest.mark.django_db(transaction=True)
class TestSciRecordAPI(BaseTestCase):
    """Test suite for the Scientific Records API"""
    
    def setUp(self):
        """Set up test client and sample data before each test"""
        super().setUp()
        self.client = APIClient()
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
            reverse('sci_record-list'),
            data=self.sample_record,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.data
        self.assertIn('id', data)
        
        # Test duplicate ID prevention
        duplicate_record = self.sample_record.copy()
        duplicate_record['id'] = data['id']
        response = self.client.post(
            reverse('sci_record-list'),
            data=duplicate_record,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid data
        invalid_record = self.sample_record.copy()
        invalid_record['air_temperature'] = "invalid"
        response = self.client.post(
            reverse('sci_record-list'),
            data=invalid_record,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_records(self):
        """Test retrieving all records"""
        # Create additional test record
        SciRecord.objects.create(
            date=date(2024, 1, 2),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=22.5,
            humidity=68.0,
            wind_speed=12.2,
            wind_direction=190.0,
            precipitation=0.2,
            haze=4.0,
            water_temperature=19.5,
            notes="Additional test record"
        )
        
        response = self.client.get(reverse('sci_record-list'))
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Including the one from setUp

    def test_get_single_record(self):
        """Test retrieving a single record by ID"""
        # Test existing record
        response = self.client.get(
            reverse('sci_record-detail', kwargs={'pk': self.test_record.id})
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.test_record.id)
        
        # Test non-existent record
        response = self.client.get(
            reverse('sci_record-detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_update_record(self):
        """Test updating an existing record"""
        update_data = self.sample_record.copy()
        update_data['air_temperature'] = 25.0
        update_data['notes'] = "Updated test record"
        
        # Test successful update
        response = self.client.put(
            reverse('sci_record-detail', kwargs={'pk': self.test_record.id}),
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['air_temperature'], 25.0)
        self.assertEqual(data['notes'], "Updated test record")
        
        # Test update of non-existent record
        response = self.client.put(
            reverse('sci_record-detail', kwargs={'pk': 99999}),
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_record(self):
        """Test deleting a record"""
        # Test successful deletion
        response = self.client.delete(
            reverse('sci_record-detail', kwargs={'pk': self.test_record.id})
        )
        self.assertEqual(response.status_code, 204)  # DRF uses 204 for successful deletion
        
        # Verify record is deleted
        with self.assertRaises(ObjectDoesNotExist):
            SciRecord.objects.get(id=self.test_record.id)
        
        # Test deleting non-existent record
        response = self.client.delete(
            reverse('sci_record-detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_bulk_delete_records(self):
        """Test deleting all records"""
        # Create additional records
        SciRecord.objects.create(
            date=date(2024, 1, 2),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=22.5,
            humidity=68.0,
            wind_speed=12.2,
            wind_direction=190.0,
            precipitation=0.2,
            haze=4.0,
            water_temperature=19.5,
            notes="Additional test record"
        )
        
        # Verify we have multiple records
        self.assertTrue(SciRecord.objects.count() > 0)
        
        # Delete all records
        response = self.client.delete(reverse('sci_record-list'))
        self.assertEqual(response.status_code, 204)  # DRF uses 204 for successful deletion
        
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
            reverse('sci_record-list'),
            data=invalid_record,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid data types
        invalid_record = self.sample_record.copy()
        invalid_record['coordinate'] = "not-an-array"
        response = self.client.post(
            reverse('sci_record-list'),
            data=invalid_record,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        
        # Test invalid date format
        invalid_record = self.sample_record.copy()
        invalid_record['date'] = "01-01-2024"  # Wrong format
        response = self.client.post(
            reverse('sci_record-list'),
            data=invalid_record,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_query_parameters(self):
        """Test filtering and querying records"""
        # Create records with different dates
        SciRecord.objects.create(
            date=date(2024, 1, 2),
            time=time(12, 0),
            time_offset=-5,
            coordinate=[40.7128, -74.0060],
            air_temperature=22.5,
            humidity=68.0,
            wind_speed=12.2,
            wind_direction=190.0,
            precipitation=0.2,
            haze=4.0,
            water_temperature=19.5,
            notes="Record for date filtering"
        )
        
        # Test date filtering
        response = self.client.get(
            f"{reverse('sci_record-list')}?date=2024-01-02"
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], '2024-01-02')
        
        # Test temperature range filtering
        response = self.client.get(
            f"{reverse('sci_record-list')}?min_temp=21&max_temp=23"
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertTrue(all(21 <= record['air_temperature'] <= 23 for record in data))

class TestSciRecordModel(BaseTestCase):
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

    def test_model_validation(self):
        """Test model field validation"""
        # Test invalid coordinate format
        with self.assertRaises(ValueError):
            SciRecord.objects.create(
                date=date(2024, 1, 1),
                time=time(12, 0),
                time_offset=-5,
                coordinate=[1, 2, 3],  # Invalid coordinate (should be [lat, lon])
                air_temperature=20.5,
                humidity=65.0,
                wind_speed=10.2,
                wind_direction=180.0,
                precipitation=0.0,
                haze=5.0,
                water_temperature=18.5,
                notes="Test invalid coordinate"
            )

class TestSciRecordSerializer(BaseTestCase):
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

    def test_validation(self):
        """Test serializer validation"""
        # Test invalid coordinate format
        invalid_data = {
            "date": "2024-01-01",
            "time": "12:00:00",
            "time_offset": -5,
            "coordinate": [1, 2, 3],  # Invalid coordinate
            "air_temperature": 20.5,
            "humidity": 65.0,
            "wind_speed": 10.2,
            "wind_direction": 180.0,
            "precipitation": 0.0,
            "haze": 5.0,
            "water_temperature": 18.5,
            "notes": "Test invalid data"
        }
        
        serializer = SciRecordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('coordinate', serializer.errors)

if __name__ == '__main__':
    pytest.main()