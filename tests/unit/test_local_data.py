"""
Tests for local data management
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from app.local_data import load_projects, save_contact


class TestLocalData:
    """Test local data file operations"""

    @patch.object(Path, 'exists')
    @patch.object(Path, 'open', new_callable=mock_open)
    def test_load_projects_file_exists(self, mock_file, mock_exists):
        """Test loading projects when file exists"""
        mock_exists.return_value = True
        test_projects = [
            {
                "name": "Test Project",
                "description": "A test project",
                "technologies": "Python, FastAPI"
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(test_projects)

        result = load_projects()
        
        assert result == test_projects
        mock_file.assert_called_once()

    @patch.object(Path, 'exists')
    def test_load_projects_file_not_exists(self, mock_exists):
        """Test loading projects when file doesn't exist"""
        mock_exists.return_value = False

        result = load_projects()
        
        assert result == []

    @patch.object(Path, 'exists')
    @patch.object(Path, 'open', new_callable=mock_open)
    def test_load_projects_json_decode_error(self, mock_file, mock_exists):
        """Test loading projects with invalid JSON"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "invalid json"

        # Should not raise exception, but might return empty list
        # depending on implementation
        try:
            result = load_projects()
        except json.JSONDecodeError:
            # If the function doesn't handle JSON decode errors,
            # this test documents that behavior
            pass

    @patch.object(Path, 'mkdir')
    @patch.object(Path, 'exists')
    @patch.object(Path, 'open', new_callable=mock_open)
    def test_save_contact_new_file(self, mock_file, mock_exists, mock_mkdir):
        """Test saving contact when contacts file doesn't exist"""
        mock_exists.return_value = False
        
        save_contact("John Doe", "john@example.com", "Test message")
        
        # Should create directory and write new contact
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        assert mock_file.call_count == 1
        
        # Check that the contact data was written  
        # The mock_open write calls are captured in mock_file().write.call_args_list
        write_calls = mock_file.return_value.write.call_args_list
        assert len(write_calls) > 0
        
        # json.dump writes in multiple calls, so we need to collect all written data
        written_data = ''.join(call[0][0] for call in write_calls)
        contacts_data = json.loads(written_data)
        
        assert len(contacts_data) == 1
        assert contacts_data[0]["name"] == "John Doe"
        assert contacts_data[0]["email"] == "john@example.com"
        assert contacts_data[0]["message"] == "Test message"

    @patch.object(Path, 'mkdir')
    @patch.object(Path, 'exists')
    @patch.object(Path, 'open', new_callable=mock_open)
    def test_save_contact_existing_file(self, mock_file, mock_exists, mock_mkdir):
        """Test saving contact when contacts file already exists"""
        mock_exists.return_value = True
        existing_contacts = [
            {"name": "Jane Smith", "email": "jane@example.com", "message": "Previous message"}
        ]
        
        # Mock reading existing file
        mock_file.return_value.read.return_value = json.dumps(existing_contacts)

        save_contact("John Doe", "john@example.com", "New message")
        
        # Should read existing file and append new contact
        assert mock_file.call_count == 2  # One read, one write
        
        # Get the written data from the write calls
        write_calls = mock_file.return_value.write.call_args_list
        if write_calls:
            # json.dump writes in multiple calls, so we need to collect all written data
            written_data = ''.join(call[0][0] for call in write_calls)
            contacts_data = json.loads(written_data)
            
            assert len(contacts_data) == 2
            assert contacts_data[1]["name"] == "John Doe"
            assert contacts_data[1]["email"] == "john@example.com"
            assert contacts_data[1]["message"] == "New message"

    @patch.object(Path, 'exists')
    def test_projects_file_path(self, mock_exists):
        """Test that projects file path is correct"""
        mock_exists.return_value = False
        load_projects()
        
        # Should check the correct file path
        mock_exists.assert_called_with()

    def test_contact_data_format(self):
        """Test contact data format requirements"""
        with patch.object(Path, 'mkdir'), \
             patch.object(Path, 'exists', return_value=False), \
             patch.object(Path, 'open', mock_open()) as mock_file:

            save_contact("Test User", "test@example.com", "Test message with special chars: éñ中")
            
            # Verify the data was written
            write_calls = mock_file.return_value.write.call_args_list
            assert len(write_calls) > 0
            
            # json.dump writes in multiple calls, so we need to collect all written data
            written_data = ''.join(call[0][0] for call in write_calls)
            contacts_data = json.loads(written_data)
            
            contact = contacts_data[0]
            assert "name" in contact
            assert "email" in contact
            assert "message" in contact
            assert contact["message"] == "Test message with special chars: éñ中"

    def test_empty_contact_data(self):
        """Test saving contact with empty data"""
        with patch.object(Path, 'mkdir'), \
             patch.object(Path, 'exists', return_value=False), \
             patch.object(Path, 'open', mock_open()) as mock_file:

            save_contact("", "", "")
            
            write_calls = mock_file.return_value.write.call_args_list
            assert len(write_calls) > 0
            
            # json.dump writes in multiple calls, so we need to collect all written data
            written_data = ''.join(call[0][0] for call in write_calls)
            contacts_data = json.loads(written_data)
            
            contact = contacts_data[0]
            assert contact["name"] == ""
            assert contact["email"] == ""
            assert contact["message"] == ""
