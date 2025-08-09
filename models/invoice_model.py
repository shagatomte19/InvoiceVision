"""
Data models for invoice structure
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class VendorInfo:
    """Vendor information structure"""
    name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }
    
    def is_empty(self) -> bool:
        """Check if vendor info is empty"""
        return not any([self.name, self.address, self.phone, self.email])

@dataclass
class BillingInfo:
    """Billing information structure"""
    name: str = ""
    address: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'address': self.address
        }
    
    def is_empty(self) -> bool:
        """Check if billing info is empty"""
        return not any([self.name, self.address])

@dataclass
class LineItem:
    """Invoice line item structure"""
    description: str = ""
    quantity: str = ""
    unit_price: str = ""
    total: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total': self.total
        }
    
    def is_empty(self) -> bool:
        """Check if line item is empty"""
        return not any([self.description, self.quantity, self.unit_price, self.total])

@dataclass
class InvoiceData:
    """Complete invoice data structure"""
    # Basic Information
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str = ""
    currency: str = ""
    
    # Financial Information
    subtotal: str = ""
    tax_amount: str = ""
    tax_rate: str = ""
    total_amount: str = ""
    
    # Entity Information
    vendor: Optional[VendorInfo] = field(default_factory=VendorInfo)
    billing_to: Optional[BillingInfo] = field(default_factory=BillingInfo)
    
    # Line Items
    line_items: List[LineItem] = field(default_factory=list)
    
    # Metadata
    raw_response: str = ""
    extraction_confidence: float = 0.0
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = {
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'currency': self.currency,
            'subtotal': self.subtotal,
            'tax_amount': self.tax_amount,
            'tax_rate': self.tax_rate,
            'total_amount': self.total_amount,
        }
        
        # Add vendor info if not empty
        if self.vendor and not self.vendor.is_empty():
            data['vendor'] = self.vendor.to_dict()
        
        # Add billing info if not empty
        if self.billing_to and not self.billing_to.is_empty():
            data['billing_to'] = self.billing_to.to_dict()
        
        # Add line items if any
        if self.line_items:
            data['line_items'] = [item.to_dict() for item in self.line_items if not item.is_empty()]
        
        # Add metadata if available
        if self.raw_response:
            data['_metadata'] = {
                'raw_response': self.raw_response,
                'extraction_confidence': self.extraction_confidence,
                'processing_time': self.processing_time
            }
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InvoiceData':
        """Create InvoiceData from dictionary"""
        invoice = cls()
        
        # Basic fields
        invoice.invoice_number = data.get('invoice_number', '')
        invoice.invoice_date = data.get('invoice_date', '')
        invoice.due_date = data.get('due_date', '')
        invoice.currency = data.get('currency', '')
        
        # Financial fields
        invoice.subtotal = data.get('subtotal', '')
        invoice.tax_amount = data.get('tax_amount', '')
        invoice.tax_rate = data.get('tax_rate', '')
        invoice.total_amount = data.get('total_amount', '')
        
        # Vendor information
        vendor_data = data.get('vendor', {})
        if vendor_data:
            invoice.vendor = VendorInfo(
                name=vendor_data.get('name', ''),
                address=vendor_data.get('address', ''),
                phone=vendor_data.get('phone', ''),
                email=vendor_data.get('email', '')
            )
        
        # Billing information
        billing_data = data.get('billing_to', {})
        if billing_data:
            invoice.billing_to = BillingInfo(
                name=billing_data.get('name', ''),
                address=billing_data.get('address', '')
            )
        
        # Line items
        line_items_data = data.get('line_items', [])
        if line_items_data:
            invoice.line_items = []
            for item_data in line_items_data:
                if isinstance(item_data, dict):
                    line_item = LineItem(
                        description=item_data.get('description', ''),
                        quantity=item_data.get('quantity', ''),
                        unit_price=item_data.get('unit_price', ''),
                        total=item_data.get('total', '')
                    )
                    invoice.line_items.append(line_item)
        
        # Metadata
        metadata = data.get('_metadata', {})
        if metadata:
            invoice.raw_response = metadata.get('raw_response', '')
            invoice.extraction_confidence = metadata.get('extraction_confidence', 0.0)
            invoice.processing_time = metadata.get('processing_time', 0.0)
        
        return invoice
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the invoice data"""
        return {
            'invoice_number': self.invoice_number,
            'vendor_name': self.vendor.name if self.vendor else '',
            'total_amount': self.total_amount,
            'currency': self.currency,
            'line_items_count': len(self.line_items),
            'has_vendor_info': self.vendor and not self.vendor.is_empty(),
            'has_billing_info': self.billing_to and not self.billing_to.is_empty(),
            'completion_rate': self._calculate_completion_rate()
        }
    
    def _calculate_completion_rate(self) -> float:
        """Calculate completion rate based on extracted fields"""
        total_fields = 0
        completed_fields = 0
        
        # Basic fields
        basic_fields = [
            self.invoice_number, self.invoice_date, self.total_amount
        ]
        for field in basic_fields:
            total_fields += 1
            if field:
                completed_fields += 1
        
        # Vendor fields
        if self.vendor:
            vendor_fields = [
                self.vendor.name, self.vendor.address, 
                self.vendor.phone, self.vendor.email
            ]
            for field in vendor_fields:
                total_fields += 1
                if field:
                    completed_fields += 1
        
        # Line items
        total_fields += 1
        if self.line_items and len(self.line_items) > 0:
            completed_fields += 1
        
        return (completed_fields / total_fields * 100) if total_fields > 0 else 0.0
    
    def validate(self) -> List[str]:
        """
        Validate invoice data and return list of validation errors
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check required fields
        if not self.invoice_number:
            errors.append("Invoice number is required")
        
        if not self.total_amount:
            errors.append("Total amount is required")
        
        # Validate date format (basic check)
        import re
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}'
        
        if self.invoice_date and not re.match(date_pattern, self.invoice_date):
            errors.append("Invoice date format may be invalid")
        
        if self.due_date and not re.match(date_pattern, self.due_date):
            errors.append("Due date format may be invalid")
        
        # Validate currency amounts
        if self.total_amount:
            try:
                float(re.sub(r'[^\d.]', '', self.total_amount))
            except ValueError:
                errors.append("Total amount is not a valid number")
        
        # Validate line items
        if self.line_items:
            for i, item in enumerate(self.line_items):
                if not item.description:
                    errors.append(f"Line item {i+1}: Description is missing")
                
                if item.unit_price:
                    try:
                        float(re.sub(r'[^\d.]', '', item.unit_price))
                    except ValueError:
                        errors.append(f"Line item {i+1}: Unit price is not a valid number")
        
        return errors
    
    def is_complete(self) -> bool:
        """Check if invoice data is reasonably complete"""
        # Must have basic information
        basic_complete = all([
            self.invoice_number,
            self.total_amount
        ])
        
        # Should have either vendor info or line items
        has_details = (
            (self.vendor and not self.vendor.is_empty()) or 
            (self.line_items and len(self.line_items) > 0)
        )
        
        return basic_complete and has_details