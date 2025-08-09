"""
Test cases for the employees dataset.

Tests the EmployeesDataset class functionality including data generation,
validation, and schema compliance.
"""

import pytest
from datetime import datetime
from tempdataset.core.datasets.employees import EmployeesDataset


class TestEmployeesDataset:
    """Test cases for EmployeesDataset class."""
    
    def test_employees_dataset_initialization(self):
        """Test that EmployeesDataset initializes correctly."""
        dataset = EmployeesDataset(rows=100)
        assert dataset.rows == 100
        assert dataset.seed is None
        assert dataset._employee_counter == 1
        assert dataset._generated_employees == []
    
    def test_employees_dataset_generate_basic(self):
        """Test basic data generation functionality."""
        dataset = EmployeesDataset(rows=10)
        data = dataset.generate()
        
        assert len(data) == 10
        assert all(isinstance(row, dict) for row in data)
    
    def test_employees_dataset_required_columns(self):
        """Test that all required columns are present."""
        dataset = EmployeesDataset(rows=5)
        data = dataset.generate()
        
        required_columns = [
            'employee_id', 'first_name', 'last_name', 'full_name', 'gender',
            'date_of_birth', 'age', 'email', 'phone_number', 'address',
            'city', 'state_province', 'country', 'postal_code', 'department',
            'job_title', 'employment_type', 'hire_date', 'termination_date',
            'years_with_company', 'manager_id', 'manager_name', 'salary_usd',
            'bonus_usd', 'total_compensation_usd', 'performance_score',
            'last_performance_review_date', 'training_hours', 'skills',
            'certifications', 'projects_count', 'current_project',
            'leave_balance_days', 'work_location', 'office_location',
            'employee_status'
        ]
        
        for row in data:
            for column in required_columns:
                assert column in row, f"Missing column: {column}"
    
    def test_employees_dataset_unique_ids(self):
        """Test that employee IDs are unique."""
        dataset = EmployeesDataset(rows=50)
        data = dataset.generate()
        
        employee_ids = [row['employee_id'] for row in data]
        assert len(employee_ids) == len(set(employee_ids)), "Employee IDs are not unique"
    
    def test_employees_dataset_id_format(self):
        """Test that employee IDs follow the correct format."""
        dataset = EmployeesDataset(rows=10)
        data = dataset.generate()
        
        for row in data:
            employee_id = row['employee_id']
            assert employee_id.startswith('EMP-'), f"Invalid employee ID format: {employee_id}"
            assert len(employee_id) == 10, f"Invalid employee ID length: {employee_id}"
            assert employee_id[4:].isdigit(), f"Invalid employee ID format: {employee_id}"
    
    def test_employees_dataset_data_types(self):
        """Test that data types are correct."""
        dataset = EmployeesDataset(rows=5)
        data = dataset.generate()
        
        for row in data:
            # String fields
            assert isinstance(row['employee_id'], str)
            assert isinstance(row['first_name'], str)
            assert isinstance(row['last_name'], str)
            assert isinstance(row['full_name'], str)
            assert isinstance(row['email'], str)
            assert isinstance(row['department'], str)
            assert isinstance(row['job_title'], str)
            
            # Integer fields
            assert isinstance(row['age'], int)
            assert isinstance(row['performance_score'], int)
            assert isinstance(row['projects_count'], int)
            
            # Float fields
            assert isinstance(row['years_with_company'], float)
            assert isinstance(row['salary_usd'], float)
            assert isinstance(row['bonus_usd'], float)
            assert isinstance(row['total_compensation_usd'], float)
            assert isinstance(row['training_hours'], float)
            assert isinstance(row['leave_balance_days'], float)
            
            # Date fields (as strings)
            assert isinstance(row['date_of_birth'], str)
            assert isinstance(row['hire_date'], str)
            assert isinstance(row['last_performance_review_date'], str)
            
            # Optional fields (can be None)
            assert row['termination_date'] is None or isinstance(row['termination_date'], str)
            assert row['manager_id'] is None or isinstance(row['manager_id'], str)
            assert row['manager_name'] is None or isinstance(row['manager_name'], str)
            assert row['certifications'] is None or isinstance(row['certifications'], str)
            assert row['current_project'] is None or isinstance(row['current_project'], str)
    
    def test_employees_dataset_date_logic(self):
        """Test that date relationships are logical."""
        dataset = EmployeesDataset(rows=20)
        data = dataset.generate()
        
        for row in data:
            hire_date = datetime.strptime(row['hire_date'], '%Y-%m-%d')
            birth_date = datetime.strptime(row['date_of_birth'], '%Y-%m-%d')
            review_date = datetime.strptime(row['last_performance_review_date'], '%Y-%m-%d')
            
            # Birth date should be before hire date
            assert birth_date < hire_date, "Birth date should be before hire date"
            
            # Review date should be after hire date
            assert review_date >= hire_date, "Review date should be after hire date"
            
            # If terminated, termination date should be after hire date
            if row['termination_date']:
                term_date = datetime.strptime(row['termination_date'], '%Y-%m-%d')
                assert term_date >= hire_date, "Termination date should be after hire date"
    
    def test_employees_dataset_compensation_logic(self):
        """Test that compensation calculations are correct."""
        dataset = EmployeesDataset(rows=10)
        data = dataset.generate()
        
        for row in data:
            salary = row['salary_usd']
            bonus = row['bonus_usd']
            total = row['total_compensation_usd']
            
            # Total compensation should equal salary + bonus
            assert abs(total - (salary + bonus)) < 0.01, "Total compensation calculation is incorrect"
            
            # All compensation values should be positive
            assert salary > 0, "Salary should be positive"
            assert bonus >= 0, "Bonus should be non-negative"
            assert total > 0, "Total compensation should be positive"
    
    def test_employees_dataset_departments_and_titles(self):
        """Test that departments and job titles are consistent."""
        dataset = EmployeesDataset(rows=30)
        data = dataset.generate()
        
        valid_departments = ['HR', 'Sales', 'Marketing', 'IT', 'Finance', 'Operations', 'R&D', 'Customer Support']
        
        for row in data:
            department = row['department']
            job_title = row['job_title']
            
            assert department in valid_departments, f"Invalid department: {department}"
            assert isinstance(job_title, str) and len(job_title) > 0, "Job title should be a non-empty string"
    
    def test_employees_dataset_manager_relationships(self):
        """Test that manager relationships are logical."""
        dataset = EmployeesDataset(rows=50)
        data = dataset.generate()
        
        # Collect all employee IDs and names
        employee_ids = {row['employee_id']: row['full_name'] for row in data}
        
        for row in data:
            manager_id = row['manager_id']
            manager_name = row['manager_name']
            
            if manager_id is not None:
                # Manager ID should exist in the dataset
                assert manager_id in employee_ids, f"Manager ID {manager_id} not found in dataset"
                
                # Manager name should match the manager ID
                assert manager_name == employee_ids[manager_id], "Manager name doesn't match manager ID"
                
                # Employee shouldn't be their own manager
                assert manager_id != row['employee_id'], "Employee cannot be their own manager"
    
    def test_employees_dataset_performance_scores(self):
        """Test that performance scores are within valid range."""
        dataset = EmployeesDataset(rows=20)
        data = dataset.generate()
        
        for row in data:
            score = row['performance_score']
            assert 1 <= score <= 5, f"Performance score {score} is not in valid range 1-5"
    
    def test_employees_dataset_age_calculation(self):
        """Test that age is calculated correctly from birth date."""
        dataset = EmployeesDataset(rows=10)
        data = dataset.generate()
        
        today = datetime.now()
        
        for row in data:
            birth_date = datetime.strptime(row['date_of_birth'], '%Y-%m-%d')
            calculated_age = int((today - birth_date).days / 365.25)
            
            # Age should be within 1 year of calculated age (accounting for leap years)
            assert abs(row['age'] - calculated_age) <= 1, "Age calculation is incorrect"
    
    def test_employees_dataset_schema(self):
        """Test that the schema is correctly defined."""
        dataset = EmployeesDataset()
        schema = dataset.get_schema()
        
        expected_columns = [
            'employee_id', 'first_name', 'last_name', 'full_name', 'gender',
            'date_of_birth', 'age', 'email', 'phone_number', 'address',
            'city', 'state_province', 'country', 'postal_code', 'department',
            'job_title', 'employment_type', 'hire_date', 'termination_date',
            'years_with_company', 'manager_id', 'manager_name', 'salary_usd',
            'bonus_usd', 'total_compensation_usd', 'performance_score',
            'last_performance_review_date', 'training_hours', 'skills',
            'certifications', 'projects_count', 'current_project',
            'leave_balance_days', 'work_location', 'office_location',
            'employee_status'
        ]
        
        assert len(schema) == len(expected_columns)
        for column in expected_columns:
            assert column in schema, f"Missing column in schema: {column}"
    
    def test_employees_dataset_reproducibility(self):
        """Test that setting a seed produces reproducible results."""
        dataset1 = EmployeesDataset(rows=10)
        dataset1.set_seed(42)
        data1 = dataset1.generate()
        
        dataset2 = EmployeesDataset(rows=10)
        dataset2.set_seed(42)
        data2 = dataset2.generate()
        
        # Data should be identical when using the same seed
        assert len(data1) == len(data2)
        for i in range(len(data1)):
            for key in data1[i]:
                assert data1[i][key] == data2[i][key], f"Data mismatch at row {i}, column {key}"
    
    def test_employees_dataset_skills_format(self):
        """Test that skills are properly formatted."""
        dataset = EmployeesDataset(rows=10)
        data = dataset.generate()
        
        for row in data:
            skills = row['skills']
            assert isinstance(skills, str), "Skills should be a string"
            assert len(skills) > 0, "Skills should not be empty"
            
            # Should contain comma-separated values
            skill_list = [skill.strip() for skill in skills.split(',')]
            assert len(skill_list) >= 1, "Should have at least one skill"
            assert all(len(skill) > 0 for skill in skill_list), "All skills should be non-empty"
    
    def test_employees_dataset_employment_status_logic(self):
        """Test that employment status is consistent with termination date."""
        dataset = EmployeesDataset(rows=30)
        data = dataset.generate()
        
        for row in data:
            status = row['employee_status']
            termination_date = row['termination_date']
            
            if status in ['Terminated', 'Retired']:
                # Should have termination date
                assert termination_date is not None, f"Employee with status {status} should have termination date"
            elif status == 'Active':
                # Should not have termination date (or it could be None)
                # Note: Some active employees might have termination_date as None, which is correct
                pass