import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CloudVitalSign
from asgiref.sync import sync_to_async

class VitalSignsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'vital_signs'
        self.room_group_name = f'vital_signs_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass # No data received from client

    async def send_vital_signs(self, event):
        vital_signs_data = event['vital_signs']
        await self.send(text_data=json.dumps(vital_signs_data))

@sync_to_async
def get_latest_vitals():
    vitals = CloudVitalSign.objects.all().order_by('-timestamp')[:10] # Get latest 10
    return list(vitals.values('patient__name', 'temperature', 'heart_rate', 'timestamp'))
