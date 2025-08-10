"""
Accounting dataset generator.

Generates realistic general ledger entries and financial statement data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class AccountingDataset(BaseDataset):
    """Accounting dataset generator for general ledger entries."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._entry_counter = 1001
        self._journal_counter = 1
    
    def _init_data_lists(self) -> None:
        self.account_types = ['Asset', 'Liability', 'Equity', 'Revenue', 'Expense']
        self.journal_types = ['Sales', 'Purchase', 'General', 'Payroll', 'Cash Receipt', 'Cash Payment']
        self.statuses = ['Draft', 'Posted', 'Approved', 'Reversed']
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
        
        self.accounts_by_type = {
            'Asset': [
                ('1001', 'Cash'), ('1002', 'Accounts Receivable'), ('1003', 'Inventory'),
                ('1004', 'Prepaid Expenses'), ('1005', 'Equipment'), ('1006', 'Buildings')
            ],
            'Liability': [
                ('2001', 'Accounts Payable'), ('2002', 'Accrued Expenses'), ('2003', 'Notes Payable'),
                ('2004', 'Mortgage Payable'), ('2005', 'Taxes Payable'), ('2006', 'Wages Payable')
            ],
            'Equity': [
                ('3001', 'Common Stock'), ('3002', 'Retained Earnings'), ('3003', 'Additional Paid-in Capital'),
                ('3004', 'Treasury Stock'), ('3005', 'Owner\'s Equity')
            ],
            'Revenue': [
                ('4001', 'Sales Revenue'), ('4002', 'Service Revenue'), ('4003', 'Interest Income'),
                ('4004', 'Rental Income'), ('4005', 'Other Income')
            ],
            'Expense': [
                ('5001', 'Cost of Goods Sold'), ('5002', 'Salaries Expense'), ('5003', 'Rent Expense'),
                ('5004', 'Utilities Expense'), ('5005', 'Advertising Expense'), ('5006', 'Insurance Expense'),
                ('5007', 'Depreciation Expense'), ('5008', 'Interest Expense')
            ]
        }
        
        self.departments = ['Sales', 'Marketing', 'Operations', 'Finance', 'HR', 'IT', 'Legal']
        self.employees = ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Wilson', 'David Brown', 'Amanda Garcia']
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Account selection
        account_type = random.choice(self.account_types)
        account_id, account_name = random.choice(self.accounts_by_type[account_type])
        
        # Transaction details
        transaction_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=365), datetime.now()
        )
        
        # Generate debit/credit amounts (one will be 0)
        amount = random.uniform(100, 50000)
        if account_type in ['Asset', 'Expense']:
            # Normal debit balance accounts
            if random.random() < 0.8:  # 80% debits for these accounts
                debit, credit = amount, 0
            else:
                debit, credit = 0, amount
        else:
            # Normal credit balance accounts (Liability, Equity, Revenue)
            if random.random() < 0.8:  # 80% credits for these accounts
                debit, credit = 0, amount
            else:
                debit, credit = amount, 0
        
        # Running balance calculation
        if account_type in ['Asset', 'Expense']:
            balance = random.uniform(1000, 100000) + debit - credit
        else:
            balance = random.uniform(1000, 100000) + credit - debit
        
        # Description generation
        descriptions = {
            'Asset': ['Cash deposit', 'Equipment purchase', 'Inventory received', 'Payment received'],
            'Liability': ['Invoice received', 'Expense accrued', 'Payment due', 'Interest accrued'],
            'Equity': ['Stock issued', 'Retained earnings', 'Capital contribution', 'Dividend declared'],
            'Revenue': ['Product sale', 'Service provided', 'Interest earned', 'Rental income'],
            'Expense': ['Office supplies', 'Salary payment', 'Utility bill', 'Insurance premium']
        }
        description = random.choice(descriptions.get(account_type, ['General transaction']))
        
        # Journal information
        journal_type = random.choice(self.journal_types)
        
        # Optional fields
        department = random.choice(self.departments) if random.random() < 0.6 else None
        project_code = f"PRJ-{random.randint(1000, 9999)}" if random.random() < 0.3 else None
        cost_center = f"CC-{random.randint(100, 999)}" if random.random() < 0.4 else None
        
        # Approval workflow
        prepared_by = random.choice(self.employees)
        approved_by = random.choice(self.employees) if random.random() < 0.7 else None
        approval_date = None
        if approved_by:
            approval_date = transaction_date + timedelta(days=random.randint(0, 7))
        
        # Status
        status = random.choice(self.statuses)
        if status == 'Draft':
            approved_by = None
            approval_date = None
        
        # Currency
        currency = random.choice(self.currencies) if random.random() < 0.1 else 'USD'
        
        # Notes
        notes = random.choice([
            'Year-end adjustment', 'Monthly accrual', 'Correcting entry', 'Reclassification',
            'Bank reconciliation', 'Audit adjustment', 'Budget variance', None
        ]) if random.random() < 0.25 else None
        
        return {
            'entry_id': f"JE-{self._entry_counter:06d}",
            'account_id': account_id,
            'account_name': account_name,
            'account_type': account_type,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'description': description,
            'debit': round(debit, 2),
            'credit': round(credit, 2),
            'balance': round(balance, 2),
            'currency': currency,
            'journal_id': f"JNL-{self._journal_counter:04d}",
            'journal_type': journal_type,
            'department': department,
            'project_code': project_code,
            'cost_center': cost_center,
            'prepared_by': prepared_by,
            'approved_by': approved_by,
            'approval_date': approval_date.strftime('%Y-%m-%d') if approval_date else None,
            'status': status,
            'notes': notes
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'entry_id': 'string', 'account_id': 'string', 'account_name': 'string',
            'account_type': 'string', 'transaction_date': 'date', 'description': 'string',
            'debit': 'float', 'credit': 'float', 'balance': 'float', 'currency': 'string',
            'journal_id': 'string', 'journal_type': 'string', 'department': 'string',
            'project_code': 'string', 'cost_center': 'string', 'prepared_by': 'string',
            'approved_by': 'string', 'approval_date': 'date', 'status': 'string', 'notes': 'string'
        }
