"""
Certificate Generator for EMIS
Generates certificates for events, workshops, and achievements
"""
from typing import Optional
from datetime import datetime, date
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
from src.lib.logging import get_logger

logger = get_logger(__name__)


class CertificateGenerator:
    """Service for generating certificates"""
    
    def __init__(self):
        self.default_template_size = (1920, 1080)  # A4 landscape at 150 DPI
        self.default_font_size = 60
        self.default_name_font_size = 80
    
    def generate_event_certificate(
        self,
        participant_name: str,
        event_title: str,
        event_date: date,
        certificate_id: str,
        organizer_name: Optional[str] = None,
        additional_text: Optional[str] = None,
        signature_url: Optional[str] = None
    ) -> BytesIO:
        """Generate event participation certificate"""
        try:
            # Create canvas
            img = Image.new('RGB', self.default_template_size, color='white')
            draw = ImageDraw.Draw(img)
            
            # Load fonts (using default PIL fonts for simplicity)
            # In production, you would use custom fonts
            title_font_size = 72
            name_font_size = 90
            text_font_size = 48
            
            # Add border
            border_color = '#1E3A8A'  # Dark blue
            border_width = 20
            draw.rectangle(
                [(border_width, border_width), 
                 (self.default_template_size[0] - border_width, 
                  self.default_template_size[1] - border_width)],
                outline=border_color,
                width=border_width
            )
            
            # Add decorative inner border
            inner_border = border_width + 40
            draw.rectangle(
                [(inner_border, inner_border), 
                 (self.default_template_size[0] - inner_border, 
                  self.default_template_size[1] - inner_border)],
                outline='#3B82F6',  # Blue
                width=5
            )
            
            # Y positions for text
            y_title = 150
            y_awarded_to = 300
            y_name = 400
            y_completion = 550
            y_event = 650
            y_date = 750
            y_signature = 880
            
            center_x = self.default_template_size[0] // 2
            
            # Certificate title
            self._draw_centered_text(
                draw, "CERTIFICATE OF PARTICIPATION",
                y_title, center_x, size=title_font_size, color='#1E3A8A'
            )
            
            # "This is to certify that"
            self._draw_centered_text(
                draw, "This is to certify that",
                y_awarded_to, center_x, size=text_font_size, color='#374151'
            )
            
            # Participant name (highlighted)
            self._draw_centered_text(
                draw, participant_name.upper(),
                y_name, center_x, size=name_font_size, color='#059669', bold=True
            )
            
            # Event completion text
            self._draw_centered_text(
                draw, "has successfully participated in",
                y_completion, center_x, size=text_font_size, color='#374151'
            )
            
            # Event title
            self._draw_centered_text(
                draw, f'"{event_title}"',
                y_event, center_x, size=text_font_size + 8, color='#1E3A8A', bold=True
            )
            
            # Event date
            formatted_date = event_date.strftime("%B %d, %Y")
            self._draw_centered_text(
                draw, f"on {formatted_date}",
                y_date, center_x, size=text_font_size, color='#374151'
            )
            
            # Add QR code with certificate ID
            qr = qrcode.QRCode(version=1, box_size=4, border=1)
            qr.add_data(f"CERT-{certificate_id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((120, 120))
            img.paste(qr_img, (100, self.default_template_size[1] - 200))
            
            # Certificate ID
            draw.text((100, self.default_template_size[1] - 60), 
                     f"Certificate ID: {certificate_id}",
                     fill='#6B7280')
            
            # Signature area (right side)
            if organizer_name:
                sig_x = self.default_template_size[0] - 400
                draw.line([(sig_x - 100, y_signature), (sig_x + 100, y_signature)], 
                         fill='#000000', width=2)
                self._draw_centered_text(
                    draw, organizer_name,
                    y_signature + 20, sig_x, size=40, color='#374151'
                )
                self._draw_centered_text(
                    draw, "Authorized Signatory",
                    y_signature + 60, sig_x, size=32, color='#6B7280'
                )
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG', quality=95)
            img_byte_arr.seek(0)
            
            logger.info(f"Certificate generated for {participant_name}")
            return img_byte_arr
            
        except Exception as e:
            logger.error(f"Error generating certificate: {str(e)}")
            raise
    
    def generate_achievement_certificate(
        self,
        recipient_name: str,
        achievement: str,
        achievement_date: date,
        certificate_id: str,
        position: Optional[str] = None,
        issuer_name: Optional[str] = None
    ) -> BytesIO:
        """Generate achievement certificate (for competitions, awards)"""
        try:
            # Similar to event certificate but with achievement focus
            img = Image.new('RGB', self.default_template_size, color='#FEF3C7')  # Light yellow
            draw = ImageDraw.Draw(img)
            
            # Gold border
            border_width = 25
            draw.rectangle(
                [(border_width, border_width), 
                 (self.default_template_size[0] - border_width, 
                  self.default_template_size[1] - border_width)],
                outline='#F59E0B',  # Gold
                width=border_width
            )
            
            center_x = self.default_template_size[0] // 2
            
            # Certificate title
            self._draw_centered_text(
                draw, "CERTIFICATE OF ACHIEVEMENT",
                150, center_x, size=72, color='#92400E'
            )
            
            # Awarded to
            self._draw_centered_text(
                draw, "This certificate is proudly presented to",
                280, center_x, size=48, color='#78350F'
            )
            
            # Recipient name
            self._draw_centered_text(
                draw, recipient_name.upper(),
                400, center_x, size=90, color='#B45309', bold=True
            )
            
            # Achievement
            if position:
                achievement_text = f"for securing {position} position in"
                self._draw_centered_text(
                    draw, achievement_text,
                    550, center_x, size=48, color='#78350F'
                )
                self._draw_centered_text(
                    draw, achievement,
                    630, center_x, size=52, color='#92400E', bold=True
                )
            else:
                self._draw_centered_text(
                    draw, f"for {achievement}",
                    580, center_x, size=52, color='#92400E', bold=True
                )
            
            # Date
            formatted_date = achievement_date.strftime("%B %d, %Y")
            self._draw_centered_text(
                draw, formatted_date,
                750, center_x, size=48, color='#78350F'
            )
            
            # QR code
            qr = qrcode.QRCode(version=1, box_size=4, border=1)
            qr.add_data(f"CERT-{certificate_id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#92400E", back_color="white")
            qr_img = qr_img.resize((120, 120))
            img.paste(qr_img, (100, self.default_template_size[1] - 200))
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG', quality=95)
            img_byte_arr.seek(0)
            
            logger.info(f"Achievement certificate generated for {recipient_name}")
            return img_byte_arr
            
        except Exception as e:
            logger.error(f"Error generating achievement certificate: {str(e)}")
            raise
    
    def _draw_centered_text(
        self, 
        draw: ImageDraw.Draw, 
        text: str, 
        y: int, 
        center_x: int, 
        size: int = 48,
        color: str = '#000000',
        bold: bool = False
    ):
        """Helper to draw centered text"""
        # Note: PIL's default font doesn't support size/bold
        # In production, use ImageFont.truetype() with actual font files
        try:
            # For now, using default font
            # Get text size (approximate)
            bbox = draw.textbbox((0, 0), text)
            text_width = bbox[2] - bbox[0]
            x = center_x - (text_width // 2)
            draw.text((x, y), text, fill=color)
        except Exception as e:
            # Fallback to left-aligned if bbox fails
            draw.text((center_x - 200, y), text, fill=color)
    
    def generate_workshop_certificate(
        self,
        participant_name: str,
        workshop_title: str,
        duration_hours: int,
        completion_date: date,
        certificate_id: str,
        instructor_name: Optional[str] = None,
        skills_learned: Optional[str] = None
    ) -> BytesIO:
        """Generate workshop completion certificate"""
        try:
            img = Image.new('RGB', self.default_template_size, color='#F0F9FF')  # Light blue
            draw = ImageDraw.Draw(img)
            
            # Blue border
            border_width = 20
            draw.rectangle(
                [(border_width, border_width), 
                 (self.default_template_size[0] - border_width, 
                  self.default_template_size[1] - border_width)],
                outline='#0369A1',
                width=border_width
            )
            
            center_x = self.default_template_size[0] // 2
            
            # Title
            self._draw_centered_text(
                draw, "WORKSHOP COMPLETION CERTIFICATE",
                130, center_x, size=68, color='#0C4A6E'
            )
            
            # Text
            self._draw_centered_text(
                draw, "This is to certify that",
                260, center_x, size=44, color='#075985'
            )
            
            # Name
            self._draw_centered_text(
                draw, participant_name.upper(),
                360, center_x, size=85, color='#0369A1', bold=True
            )
            
            # Workshop
            self._draw_centered_text(
                draw, "has successfully completed the workshop on",
                510, center_x, size=44, color='#075985'
            )
            
            self._draw_centered_text(
                draw, f'"{workshop_title}"',
                600, center_x, size=50, color='#0C4A6E', bold=True
            )
            
            # Duration
            self._draw_centered_text(
                draw, f"Duration: {duration_hours} hours",
                700, center_x, size=42, color='#075985'
            )
            
            # Date
            formatted_date = completion_date.strftime("%B %d, %Y")
            self._draw_centered_text(
                draw, f"Completed on: {formatted_date}",
                770, center_x, size=42, color='#075985'
            )
            
            # QR code
            qr = qrcode.QRCode(version=1, box_size=4, border=1)
            qr.add_data(f"CERT-{certificate_id}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#0C4A6E", back_color="white")
            qr_img = qr_img.resize((120, 120))
            img.paste(qr_img, (100, self.default_template_size[1] - 200))
            
            # Instructor signature if provided
            if instructor_name:
                sig_x = self.default_template_size[0] - 400
                draw.line([(sig_x - 100, 900), (sig_x + 100, 900)], 
                         fill='#000000', width=2)
                self._draw_centered_text(
                    draw, instructor_name,
                    920, sig_x, size=40, color='#075985'
                )
                self._draw_centered_text(
                    draw, "Workshop Instructor",
                    960, sig_x, size=32, color='#6B7280'
                )
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG', quality=95)
            img_byte_arr.seek(0)
            
            logger.info(f"Workshop certificate generated for {participant_name}")
            return img_byte_arr
            
        except Exception as e:
            logger.error(f"Error generating workshop certificate: {str(e)}")
            raise
