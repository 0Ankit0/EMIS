"""PDF Generation Utilities for EMIS"""
from datetime import datetime
from typing import Optional, List, Dict
from io import BytesIO
import os
import qrcode

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart

from src.models.billing import Bill
from src.models.reports import QuarterlyReport
from src.lib.logging import get_logger

logger = get_logger(__name__)


class PDFGenerator:
    """Utility class for generating PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            spaceAfter=12
        )
    
    def generate_qr_code(
        self,
        data: str,
        size: int = 150
    ) -> Image:
        """Generate QR code image for payment or reference
        
        Args:
            data: The data to encode in QR code (payment URL, bill reference, etc.)
            size: Size of the QR code in pixels
            
        Returns:
            ReportLab Image object containing the QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Create ReportLab Image
        qr_img = Image(buffer, width=size, height=size)
        
        return qr_img
    
    def generate_bill_pdf(
        self,
        bill: Bill,
        filepath: str,
        institution_name: str = "Educational Institution",
        institution_address: str = "",
        institution_logo: Optional[str] = None
    ) -> str:
        """Generate PDF for a bill"""
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Header with institution info
        if institution_logo and os.path.exists(institution_logo):
            logo = Image(institution_logo, width=1*inch, height=1*inch)
            story.append(logo)
            story.append(Spacer(1, 0.2*inch))
        
        # Institution name
        story.append(Paragraph(institution_name, self.title_style))
        
        if institution_address:
            story.append(Paragraph(institution_address, self.body_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Bill title
        story.append(Paragraph(f"<b>BILL - {bill.bill_number}</b>", self.heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Bill details
        bill_details = [
            ['Bill Number:', bill.bill_number],
            ['Bill Date:', bill.bill_date.strftime('%d-%b-%Y')],
            ['Due Date:', bill.due_date.strftime('%d-%b-%Y')],
            ['Bill Type:', bill.bill_type.value.replace('_', ' ').title()],
            ['Status:', bill.status.value.title()],
        ]
        
        if bill.academic_year:
            bill_details.append(['Academic Year:', bill.academic_year])
        if bill.semester:
            bill_details.append(['Semester:', str(bill.semester)])
        
        details_table = Table(bill_details, colWidths=[2*inch, 4*inch])
        details_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Items table
        story.append(Paragraph('<b>Bill Items</b>', self.heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        items_data = [['#', 'Description', 'Qty', 'Unit Price', 'Amount']]
        
        for idx, item in enumerate(bill.items, 1):
            items_data.append([
                str(idx),
                item.item_name,
                f"{item.quantity:.2f}",
                f"₹{item.unit_price:,.2f}",
                f"₹{item.amount:,.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3*inch, 0.75*inch, 1.25*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        summary_data = [
            ['Subtotal:', f"₹{bill.subtotal:,.2f}"],
            ['Tax:', f"₹{bill.tax_amount:,.2f}"],
            ['Discount:', f"₹{bill.discount_amount:,.2f}"],
            ['<b>Total Amount:</b>', f"<b>₹{bill.total_amount:,.2f}</b>"],
            ['Amount Paid:', f"₹{bill.amount_paid:,.2f}"],
            ['<b>Amount Due:</b>', f"<b>₹{bill.amount_due:,.2f}</b>"],
        ]
        
        summary_table = Table(summary_data, colWidths=[4.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),
            ('LINEABOVE', (0, 5), (-1, 5), 2, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Notes
        if bill.notes:
            story.append(Paragraph('<b>Notes:</b>', self.body_style))
            story.append(Paragraph(bill.notes, self.body_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Terms and conditions
        if bill.terms_and_conditions:
            story.append(Paragraph('<b>Terms and Conditions:</b>', self.body_style))
            story.append(Paragraph(bill.terms_and_conditions, self.body_style))
        
        # QR Code for online payment (if bill is unpaid)
        if bill.amount_due > 0:
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph('<b>Pay Online:</b>', self.body_style))
            
            # Generate payment URL/reference for QR code
            payment_data = f"BILL:{bill.bill_number}|AMOUNT:{bill.amount_due}|DUE:{bill.due_date.strftime('%Y-%m-%d')}"
            qr_image = self.generate_qr_code(payment_data, size=100)
            
            story.append(qr_image)
            story.append(Paragraph(
                '<i>Scan this QR code to pay online</i>', 
                ParagraphStyle('QRNote', fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
            ))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = f"Generated on {datetime.now().strftime('%d-%b-%Y %I:%M %p')}"
        story.append(Paragraph(footer_text, ParagraphStyle('Footer', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(story)
        
        logger.info(f"Generated bill PDF: {filepath}")
        
        return filepath
    
    def generate_quarterly_report_pdf(
        self,
        report: QuarterlyReport,
        filepath: str,
        institution_name: str = "Educational Institution"
    ) -> str:
        """Generate PDF for quarterly report"""
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph(institution_name, self.title_style))
        story.append(Spacer(1, 0.1*inch))
        
        report_title = f"Quarterly Financial Report - Q{report.quarter} {report.financial_year}"
        story.append(Paragraph(report_title, self.heading_style))
        
        period = f"{report.start_date.strftime('%d %b %Y')} to {report.end_date.strftime('%d %b %Y')}"
        story.append(Paragraph(period, self.body_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph('<b>Executive Summary</b>', self.heading_style))
        
        summary_data = [
            ['Total Income', f"₹{report.total_income:,.2f}"],
            ['Total Expenses', f"₹{report.total_expenses:,.2f}"],
            ['<b>Net Profit/Loss</b>', f"<b>₹{report.net_profit_loss:,.2f}</b>"],
            ['Students', str(report.student_count)],
            ['Employees', str(report.employee_count)],
            ['Fee Collection Rate', f"{report.fee_collection_rate:.1f}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 2), (-1, 2), 'Helvetica-Bold', 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f5e9')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffebee')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e3f2fd')),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Income Breakdown
        story.append(Paragraph('<b>Income Breakdown</b>', self.heading_style))
        
        income_data = [
            ['Tuition Fees', f"₹{report.tuition_fee_income:,.2f}"],
            ['Admission Fees', f"₹{report.admission_fee_income:,.2f}"],
            ['Exam Fees', f"₹{report.exam_fee_income:,.2f}"],
            ['Library Fees', f"₹{report.library_fee_income:,.2f}"],
            ['Other Fees', f"₹{report.other_fee_income:,.2f}"],
            ['Miscellaneous', f"₹{report.miscellaneous_income:,.2f}"],
            ['<b>Total</b>', f"<b>₹{report.total_income:,.2f}</b>"],
        ]
        
        income_table = Table(income_data, colWidths=[3*inch, 3*inch])
        income_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(income_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Expense Breakdown
        story.append(Paragraph('<b>Expense Breakdown</b>', self.heading_style))
        
        expense_data = [
            ['Salaries', f"₹{report.salary_expenses:,.2f}"],
            ['Maintenance', f"₹{report.maintenance_expenses:,.2f}"],
            ['Utilities', f"₹{report.utility_expenses:,.2f}"],
            ['Infrastructure', f"₹{report.infrastructure_expenses:,.2f}"],
            ['Administrative', f"₹{report.administrative_expenses:,.2f}"],
            ['Emergency', f"₹{report.emergency_expenses:,.2f}"],
            ['Other', f"₹{report.other_expenses:,.2f}"],
            ['<b>Total</b>', f"<b>₹{report.total_expenses:,.2f}</b>"],
        ]
        
        expense_table = Table(expense_data, colWidths=[3*inch, 3*inch])
        expense_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(expense_table)
        
        # Build PDF
        doc.build(story)
        
        logger.info(f"Generated quarterly report PDF: {filepath}")
        
        return filepath
