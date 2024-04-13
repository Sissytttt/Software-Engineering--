from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from .models import BusinessOwner, Place, Event, Client

class CityConnectEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Client):
            return {
                'type': 'Client',
                'phone_number': obj.phone_number,
                'city': obj.city,
                'follows': obj.follows,
                'follows_count': len(obj.get_follows()),
                'added_places_count' : len(obj.get_added_places()),
                'added_events_count': len(obj.get_added_events()),
                'email': obj.auth.email,
                'username': obj.auth.username,
            }
        
        if isinstance(obj, Place):
            return {
                'type': 'Place',
                'id': obj.id,
                'name': obj.name,
                'longitude': obj.longitude,
                'latitude': obj.latitude,
                'city': obj.city,
            }

        if isinstance(obj, Event):
            return {
                'id': obj.id,
                'name': obj.name,
                'place': obj.place,
                'business_owner': obj.business_owner,
                'start_time': obj.start_time,
                'end_time': obj.end_time,
                'description': obj.description,
                'max_ppl': obj.max_ppl,
                'current_ppl_count': len(obj.get_current_ppl()),
                'score': obj.score,
                'avg_price': obj.avg_price,
                'event_type': obj.event_type,
                'ppl_reviewed': obj.ppl_reviewed,
            }
            
        if isinstance(obj, BusinessOwner):
            return {
                'type': 'BusinessOwner',
                'phone': obj.phone,
                'city': obj.city,
            }

        return super().default(obj)
