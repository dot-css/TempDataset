"""
Employees dataset generator.

Generates realistic employee data with comprehensive HR information including
personal details, employment information, compensation, and performance metrics.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class EmployeesDataset(BaseDataset):
    """
    Employees dataset generator that creates realistic employee HR data.
    
    Generates comprehensive employee data including:
    - Personal information (names, demographics, contact details)
    - Employment details (hire dates, departments, job titles)
    - Compensation (salary, bonus, total compensation)
    - Performance metrics (scores, reviews, training)
    - Work arrangements (location, status, projects)
    - Management hierarchy (manager relationships)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the EmployeesDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential employee IDs
        self._employee_counter = 1
        
        # Store generated employees for manager relationships
        self._generated_employees = []
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Departments and their typical job titles
        self.departments = {
            'HR': ['HR Manager', 'HR Specialist', 'Recruiter', 'HR Coordinator', 'Benefits Administrator'],
            'Sales': ['Sales Manager', 'Sales Representative', 'Account Executive', 'Sales Coordinator', 'Business Development Manager'],
            'Marketing': ['Marketing Manager', 'Marketing Specialist', 'Content Creator', 'Digital Marketing Manager', 'Brand Manager'],
            'IT': ['Software Engineer', 'DevOps Engineer', 'Data Analyst', 'IT Manager', 'System Administrator', 'QA Engineer'],
            'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'Controller', 'Budget Analyst'],
            'Operations': ['Operations Manager', 'Operations Coordinator', 'Process Analyst', 'Supply Chain Manager', 'Logistics Coordinator'],
            'R&D': ['Research Scientist', 'Product Manager', 'R&D Engineer', 'Innovation Manager', 'Technical Lead'],
            'Customer Support': ['Customer Support Representative', 'Support Manager', 'Technical Support Specialist', 'Customer Success Manager']
        }
        
        # Employment types
        self.employment_types = ['Full-time', 'Part-time', 'Contract', 'Internship']
        
        # Gender options
        self.genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
        
        # Work locations
        self.work_locations = ['Onsite', 'Remote', 'Hybrid']
        
        # Office locations (cities)
        self.office_locations = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
            'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
            'Seattle', 'Denver', 'Boston', 'Nashville', 'Detroit', 'Portland',
            'Las Vegas', 'Memphis', 'Louisville', 'Baltimore', 'Milwaukee', 'Atlanta'
        ]
        
        # Employee statuses
        self.employee_statuses = ['Active', 'On Leave', 'Terminated', 'Retired']
        
        # Common skills by department
        self.skills_by_department = {
            'HR': ['Recruitment', 'Employee Relations', 'Performance Management', 'Benefits Administration', 'Training & Development'],
            'Sales': ['Lead Generation', 'CRM', 'Negotiation', 'Customer Relationship Management', 'Sales Forecasting'],
            'Marketing': ['Digital Marketing', 'Content Creation', 'SEO', 'Social Media', 'Brand Management', 'Analytics'],
            'IT': ['Python', 'Java', 'JavaScript', 'SQL', 'Cloud Computing', 'DevOps', 'Data Analysis', 'Cybersecurity'],
            'Finance': ['Financial Analysis', 'Budgeting', 'Forecasting', 'Excel', 'Financial Reporting', 'Risk Management'],
            'Operations': ['Process Improvement', 'Project Management', 'Supply Chain', 'Logistics', 'Quality Assurance'],
            'R&D': ['Research', 'Product Development', 'Innovation', 'Technical Writing', 'Data Analysis', 'Project Management'],
            'Customer Support': ['Customer Service', 'Technical Support', 'Problem Solving', 'Communication', 'CRM']
        }
        
        # Common certifications by department
        self.certifications_by_department = {
            'HR': ['PHR', 'SHRM-CP', 'SHRM-SCP', 'HRCI'],
            'Sales': ['Salesforce Certified', 'HubSpot Certified', 'Google Analytics'],
            'Marketing': ['Google Ads Certified', 'HubSpot Marketing', 'Facebook Blueprint', 'Google Analytics'],
            'IT': ['AWS Solutions Architect', 'Microsoft Azure', 'Cisco CCNA', 'CompTIA Security+', 'PMP'],
            'Finance': ['CPA', 'CFA', 'FRM', 'CMA'],
            'Operations': ['PMP', 'Six Sigma', 'Lean Manufacturing', 'APICS'],
            'R&D': ['PMP', 'Agile Certified', 'Six Sigma'],
            'Customer Support': ['ITIL', 'Customer Service Certification', 'Technical Support Certification']
        }
        
        # Project names
        self.project_names = [
            'Digital Transformation Initiative', 'Customer Experience Enhancement', 'Product Launch 2024',
            'Process Optimization', 'Market Expansion', 'Technology Upgrade', 'Quality Improvement',
            'Cost Reduction Program', 'Innovation Lab', 'Sustainability Initiative', 'Data Analytics Platform',
            'Mobile App Development', 'Cloud Migration', 'Security Enhancement', 'Training Program'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate employees dataset rows.
        
        Returns:
            List of dictionaries representing employee records
        """
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        data = []
        
        # First pass: generate all employees without manager relationships
        for i in range(self.rows):
            row = self._generate_row()
            data.append(row)
            self._generated_employees.append({
                'employee_id': row['employee_id'],
                'full_name': row['full_name'],
                'department': row['department'],
                'job_title': row['job_title']
            })
        
        # Second pass: assign managers (about 80% of employees have managers)
        self._assign_managers(data)
        
        return data
    
    def _generate_row(self) -> Dict[str, Any]:
        """Generate a single employee record."""
        
        # Generate personal information
        first_name = self.faker_utils.first_name()
        last_name = self.faker_utils.last_name()
        full_name = f"{first_name} {last_name}"
        
        # Generate birth date (employees aged 22-65)
        today = datetime.now()
        min_birth_date = today - timedelta(days=65*365)
        max_birth_date = today - timedelta(days=22*365)
        date_of_birth = self.faker_utils.date_between(min_birth_date, max_birth_date)
        
        # Convert date_of_birth to datetime for calculation if it's a date object
        if hasattr(date_of_birth, 'date'):
            # It's already a datetime
            birth_datetime = date_of_birth
        else:
            # It's a date, convert to datetime
            birth_datetime = datetime.combine(date_of_birth, datetime.min.time())
        
        age = int((today - birth_datetime).days / 365.25)
        
        # Generate contact information
        email = self.faker_utils.email(full_name)
        phone_number = self.faker_utils.phone_number()
        address = self.faker_utils.address().replace('\n', ', ')
        city = self.faker_utils.city()
        state_province = self.faker_utils.state()
        country = self.faker_utils.country()
        postal_code = self.faker_utils.postal_code()
        
        # Generate employment information
        department = random.choice(list(self.departments.keys()))
        job_title = random.choice(self.departments[department])
        employment_type = random.choice(self.employment_types)
        
        # Generate hire date (within last 10 years, but not future)
        max_hire_date = min(today, today - timedelta(days=30))  # At least 30 days ago
        min_hire_date = today - timedelta(days=10*365)
        hire_date = self.faker_utils.date_between(min_hire_date, max_hire_date)
        
        # Generate termination date (20% chance of being terminated)
        termination_date = None
        employee_status = 'Active'
        if random.random() < 0.20:
            # Terminated employees
            # Convert hire_date to datetime for calculation if it's a date object
            if hasattr(hire_date, 'date'):
                hire_datetime_for_term = hire_date
            else:
                hire_datetime_for_term = datetime.combine(hire_date, datetime.min.time())
            
            min_term_date = hire_datetime_for_term + timedelta(days=30)  # At least 30 days after hire
            max_term_date = today
            if min_term_date < max_term_date:
                termination_date = self.faker_utils.date_between(min_term_date, max_term_date)
                employee_status = random.choice(['Terminated', 'Retired'])
        elif random.random() < 0.05:
            # 5% on leave
            employee_status = 'On Leave'
        
        # Calculate years with company
        end_date = termination_date if termination_date else today
        
        # Convert hire_date to datetime for calculation if it's a date object
        if hasattr(hire_date, 'date'):
            # It's already a datetime
            hire_datetime = hire_date
        else:
            # It's a date, convert to datetime
            hire_datetime = datetime.combine(hire_date, datetime.min.time())
        
        # Convert end_date to datetime for calculation if it's a date object
        if hasattr(end_date, 'date'):
            # It's already a datetime
            end_datetime = end_date
        else:
            # It's a date, convert to datetime
            end_datetime = datetime.combine(end_date, datetime.min.time())
        
        years_with_company = round((end_datetime - hire_datetime).days / 365.25, 1)
        
        # Generate compensation based on department and seniority
        salary_usd = self._generate_salary(department, job_title, years_with_company)
        bonus_usd = round(salary_usd * random.uniform(0.05, 0.20), 2)  # 5-20% bonus
        total_compensation_usd = salary_usd + bonus_usd
        
        # Generate performance metrics
        performance_score = random.randint(1, 5)
        
        # Generate last performance review date
        if employee_status == 'Active':
            # Convert hire_date to datetime for comparison
            if hasattr(hire_date, 'date'):
                hire_datetime_for_review = hire_date
            else:
                hire_datetime_for_review = datetime.combine(hire_date, datetime.min.time())
            
            review_start = max(hire_datetime_for_review, today - timedelta(days=365))
            last_performance_review_date = self.faker_utils.date_between(review_start, today)
        else:
            # For terminated employees, review before termination
            review_end = termination_date if termination_date else today
            
            # Convert dates to datetime for comparison
            if hasattr(hire_date, 'date'):
                hire_datetime_for_review = hire_date
            else:
                hire_datetime_for_review = datetime.combine(hire_date, datetime.min.time())
            
            if hasattr(review_end, 'date'):
                review_end_datetime = review_end
            else:
                review_end_datetime = datetime.combine(review_end, datetime.min.time())
            
            review_start = max(hire_datetime_for_review, review_end_datetime - timedelta(days=365))
            if review_start < review_end_datetime:
                last_performance_review_date = self.faker_utils.date_between(review_start, review_end_datetime)
            else:
                last_performance_review_date = hire_date
        
        # Generate training and skills
        training_hours = round(random.uniform(0, 80), 1)  # 0-80 hours per year
        skills = self._generate_skills(department)
        certifications = self._generate_certifications(department)
        
        # Generate project information
        projects_count = random.randint(0, 8)
        current_project = random.choice(self.project_names) if employee_status == 'Active' and random.random() < 0.7 else None
        
        # Generate work arrangement
        leave_balance_days = round(random.uniform(0, 25), 1)  # 0-25 days
        work_location = random.choice(self.work_locations)
        office_location = random.choice(self.office_locations)
        
        return {
            'employee_id': self._generate_employee_id(),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': full_name,
            'gender': random.choice(self.genders),
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
            'age': age,
            'email': email,
            'phone_number': phone_number,
            'address': address,
            'city': city,
            'state_province': state_province,
            'country': country,
            'postal_code': postal_code,
            'department': department,
            'job_title': job_title,
            'employment_type': employment_type,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'termination_date': termination_date.strftime('%Y-%m-%d') if termination_date else None,
            'years_with_company': years_with_company,
            'manager_id': None,  # Will be assigned in second pass
            'manager_name': None,  # Will be assigned in second pass
            'salary_usd': salary_usd,
            'bonus_usd': bonus_usd,
            'total_compensation_usd': total_compensation_usd,
            'performance_score': performance_score,
            'last_performance_review_date': last_performance_review_date.strftime('%Y-%m-%d'),
            'training_hours': training_hours,
            'skills': skills,
            'certifications': certifications,
            'projects_count': projects_count,
            'current_project': current_project,
            'leave_balance_days': leave_balance_days,
            'work_location': work_location,
            'office_location': office_location,
            'employee_status': employee_status
        }
    
    def _generate_employee_id(self) -> str:
        """
        Generate employee ID in format "EMP-NNNNNN".
        
        Returns:
            Formatted employee ID
        """
        employee_num = str(self._employee_counter).zfill(6)
        self._employee_counter += 1
        return f"EMP-{employee_num}"
    
    def _generate_salary(self, department: str, job_title: str, years_with_company: float) -> float:
        """
        Generate realistic salary based on department, role, and experience.
        
        Args:
            department: Employee's department
            job_title: Employee's job title
            years_with_company: Years of experience
            
        Returns:
            Annual salary in USD
        """
        # Base salary ranges by department
        base_ranges = {
            'HR': (45000, 85000),
            'Sales': (40000, 120000),
            'Marketing': (45000, 95000),
            'IT': (60000, 140000),
            'Finance': (50000, 110000),
            'Operations': (45000, 90000),
            'R&D': (65000, 130000),
            'Customer Support': (35000, 70000)
        }
        
        # Manager roles get higher salaries
        is_manager = 'Manager' in job_title or 'Lead' in job_title
        
        min_salary, max_salary = base_ranges.get(department, (40000, 80000))
        
        if is_manager:
            min_salary = int(min_salary * 1.3)
            max_salary = int(max_salary * 1.5)
        
        # Base salary
        base_salary = random.uniform(min_salary, max_salary)
        
        # Experience multiplier (up to 50% increase for 10+ years)
        experience_multiplier = 1 + min(years_with_company * 0.05, 0.5)
        
        final_salary = base_salary * experience_multiplier
        
        return round(final_salary, 2)
    
    def _generate_skills(self, department: str) -> str:
        """
        Generate comma-separated skills based on department.
        
        Args:
            department: Employee's department
            
        Returns:
            Comma-separated string of skills
        """
        dept_skills = self.skills_by_department.get(department, ['Communication', 'Teamwork', 'Problem Solving'])
        
        # Select 3-6 skills
        num_skills = random.randint(3, 6)
        selected_skills = random.sample(dept_skills, min(num_skills, len(dept_skills)))
        
        # Add some general skills
        general_skills = ['Communication', 'Teamwork', 'Problem Solving', 'Time Management', 'Leadership']
        if random.random() < 0.3:  # 30% chance to add a general skill
            general_skill = random.choice(general_skills)
            if general_skill not in selected_skills:
                selected_skills.append(general_skill)
        
        return ', '.join(selected_skills)
    
    def _generate_certifications(self, department: str) -> Optional[str]:
        """
        Generate certifications based on department (60% chance of having certifications).
        
        Args:
            department: Employee's department
            
        Returns:
            Comma-separated string of certifications or None
        """
        if random.random() > 0.6:  # 40% chance of no certifications
            return None
        
        dept_certs = self.certifications_by_department.get(department, [])
        if not dept_certs:
            return None
        
        # Select 1-3 certifications
        num_certs = random.randint(1, min(3, len(dept_certs)))
        selected_certs = random.sample(dept_certs, num_certs)
        
        return ', '.join(selected_certs)
    
    def _assign_managers(self, data: List[Dict[str, Any]]) -> None:
        """
        Assign managers to employees in a second pass.
        
        Args:
            data: List of employee records to update with manager information
        """
        # Group employees by department
        dept_employees = {}
        for i, employee in enumerate(data):
            dept = employee['department']
            if dept not in dept_employees:
                dept_employees[dept] = []
            dept_employees[dept].append((i, employee))
        
        # For each department, assign managers
        for dept, employees in dept_employees.items():
            if len(employees) <= 1:
                continue  # Skip departments with only one employee
            
            # Find potential managers (those with manager titles or senior roles)
            managers = []
            non_managers = []
            
            for idx, emp in employees:
                if ('Manager' in emp['job_title'] or 'Lead' in emp['job_title'] or 
                    emp['years_with_company'] >= 3):
                    managers.append((idx, emp))
                else:
                    non_managers.append((idx, emp))
            
            # If no managers found, promote the most senior employee
            if not managers and employees:
                # Sort by years with company, descending
                sorted_employees = sorted(employees, key=lambda x: x[1]['years_with_company'], reverse=True)
                managers = [sorted_employees[0]]
                non_managers = sorted_employees[1:]
            
            # Assign managers to non-managers (80% chance)
            for idx, emp in non_managers:
                if random.random() < 0.8 and managers:  # 80% chance of having a manager
                    manager_idx, manager = random.choice(managers)
                    data[idx]['manager_id'] = manager['employee_id']
                    data[idx]['manager_name'] = manager['full_name']
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'employee_id': 'string',
            'first_name': 'string',
            'last_name': 'string',
            'full_name': 'string',
            'gender': 'string',
            'date_of_birth': 'date',
            'age': 'integer',
            'email': 'string',
            'phone_number': 'string',
            'address': 'string',
            'city': 'string',
            'state_province': 'string',
            'country': 'string',
            'postal_code': 'string',
            'department': 'string',
            'job_title': 'string',
            'employment_type': 'string',
            'hire_date': 'date',
            'termination_date': 'date',
            'years_with_company': 'float',
            'manager_id': 'string',
            'manager_name': 'string',
            'salary_usd': 'float',
            'bonus_usd': 'float',
            'total_compensation_usd': 'float',
            'performance_score': 'integer',
            'last_performance_review_date': 'date',
            'training_hours': 'float',
            'skills': 'string',
            'certifications': 'string',
            'projects_count': 'integer',
            'current_project': 'string',
            'leave_balance_days': 'float',
            'work_location': 'string',
            'office_location': 'string',
            'employee_status': 'string'
        }