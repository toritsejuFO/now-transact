from app.utility import Response
from app.services import login_required

@login_required
def search(decoded_payload):
    print(decoded_payload)
    return Response.success('Got here'), 200
