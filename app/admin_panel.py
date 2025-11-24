from sqladmin import Admin, ModelView
from app.db.models import Gate, ParkingSlot, ParkingTicketSession

class GateAdmin(ModelView, model=Gate):
    name = "Cổng (Gate)"
    name_plural = "Quản lý Cổng"
    icon = "fa-solid fa-door-open" 
    column_list = [Gate.id, Gate.name] 

class SlotAdmin(ModelView, model=ParkingSlot):
    name = "Chỗ Đỗ (Slot)"
    name_plural = "Quản lý Chỗ Đỗ"
    icon = "fa-solid fa-square-parking"
    column_list = [ParkingSlot.id, ParkingSlot.slot_code, ParkingSlot.status]
    column_sortable_list = [ParkingSlot.status] 

class TicketAdmin(ModelView, model=ParkingTicketSession):
    name = "Vé Xe (Ticket)"
    name_plural = "Lịch sử Ra/Vào"
    icon = "fa-solid fa-ticket"
    column_list = [
        ParkingTicketSession.session_id,
        ParkingTicketSession.status,
        ParkingTicketSession.fail_auth_count, 
        ParkingTicketSession.entry_time,
        ParkingTicketSession.exit_time
    ]
    column_default_sort = ("entry_time", True) 

def setup_admin(app, engine):
    admin = Admin(app, engine, title="Smart Parking Admin")
    admin.add_view(GateAdmin)
    admin.add_view(SlotAdmin)
    admin.add_view(TicketAdmin)