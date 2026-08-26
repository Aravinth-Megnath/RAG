from langchain_core.tools import tool


from database.database import session_local
from database.schemas import CreateReservation
from services_reservation.reservation_services import ReservationService

@tool
def create_reservation(
        guest_name:str,
        email:str,
        check_in:str,
        check_out:str,
        room_preference:str | None = None
):
    """
     Create a hotel reservation.

     Use this tool only when all required reservation details are available.

     Required:
     -guest_name
     -email
     -check_in
     -check_out
     
     Do not create a reservation if any of the required details are missing.
       Instead, ask the user for the missing information.
    
    Optional:
    -room_preference
    """

    try:
        reservation_data = CreateReservation(
            guest_name=guest_name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            room_preference=room_preference
        )
        db = session_local()

        try:
            reservation = ReservationService.create_reservation(db, reservation_data)
            return {
                'success': True,
                'reservation_id' : reservation.id,
                'status': reservation.status,
                'message': 'Reservation created successfully.'
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'success': False,
            'message': f'Error creating reservation: {str(e)}'
        }


@tool
def get_reservation(reservation_id:int, email:str):
    '''Retrieve a reservation using the reservation ID and 
    the email address associated with the reservation.'''

    try:
        db = session_local()
        try:
            reservation = ReservationService.get_reservation(
                db, reservation_id,email
            )

            if reservation is None:
                return {
                    'success': False,
                    'message': 'Reservation not found.'
                }
            return {
                'success': True,
                'reservation_id': reservation.id,
                # 'guest_name': reservation.guest_name,
                'check_in':str(reservation.check_in),
                'check_out':str(reservation.check_out),
                'room_preference': reservation.room_preference,
                'status':reservation.status
            }
        finally:
            db.close()
    except Exception as e:
        return{
            'success':False,
            'message': 'Unable to retrieve the reservation with the provided details'
        }

@tool
def cancel_reservation(reservation_id:int, email:str):
    '''Cancel a reservation using the reservation ID and the 
       email address associated with the reservation.'''

    try:
        db = session_local()
        try:
            reservation = ReservationService.cancel_reservation(
                db, reservation_id,email
            )
            if reservation is None:
                return {
                    'success': False,
                    'message': 'Reservation not found or already cancelled.'
                }
            return {
                'success': True,
                'reservation_id': reservation.id,
                'status': reservation.status,
                'message': 'Reservation cancelled successfully.'}
        finally:
            db.close()
    except Exception as e:
        return {
            'success': False,
            'message': 'Unable to cancel the reservation'
        }


tools = [create_reservation, get_reservation, cancel_reservation]
tool_map = {
    tool.name:tool for tool in tools    
}
















































