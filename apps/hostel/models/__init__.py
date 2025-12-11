from .hostel import Hostel
from .floor import Floor
from .room import Room
from .room_allocation import RoomAllocation
from .hostel_fee import HostelFee
from .mess_menu import MessMenu
from .visitor_log import VisitorLog
from .complaint import Complaint
from .outing_request import OutingRequest
from .attendance import Attendance
from ..managers import HostelManager, RoomManager, RoomAllocationManager, ComplaintManager, OutingRequestManager

Hostel.add_to_class('objects', HostelManager())
Room.add_to_class('objects', RoomManager())
RoomAllocation.add_to_class('objects', RoomAllocationManager())
Complaint.add_to_class('objects', ComplaintManager())
OutingRequest.add_to_class('objects', OutingRequestManager())
