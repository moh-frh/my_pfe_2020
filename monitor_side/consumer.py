from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync

class DashConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.groupname = 'dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

# send the actual message
    async def deprocessing(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({
            'value': valOther,

        }))

    async def deprocessing2(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({
            'value2': valOther,

        }))

    async def deprocessing3(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({
            'value3': valOther,

        }))

    async def deprocessing4(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({
            'value4': valOther,

        }))


    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        # print("text_data : ", datapoint["type"])

        # val = datapoint['value']
        # print("val de graph1", val)
        #
        # # broadcast the message event to be sent
        # await self.channel_layer.group_send(
        #     self.groupname,
        #     {
        #         'type': 'deprocessing2',
        #         'value': val
        #     }
        # )

        if (datapoint["type"] == "graph2"):

            val = datapoint['value']
            # print("val de graph1", val)

            # broadcast the message event to be sent
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'deprocessing2',
                    'value': val
                }
            )

        elif(datapoint["type"] == "graph1"):
            val = datapoint['value']
            # print("val de graph1", val)

            # broadcast the message event to be sent
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'deprocessing',
                    'value': val
                }
            )
        elif(datapoint["type"] == "graph3"):
            val = datapoint['value']
            # print("val de graph3", val)

            # broadcast the message event to be sent
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'deprocessing3',
                    'value': val
                }
            )

        else:
            val = datapoint['value']
            # print("val de graph4", val)

            # broadcast the message event to be sent
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'deprocessing4',
                    'value': val
                }
            )

            # on est dans graph2
        # elif (datapoint["type"] == "graph2"):
        #     print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
        #
        #     val2 = datapoint['value']
        #     print("val de graph2", val2)
        #
        #     # broadcast the message event to be sent
        #     await self.channel_layer.group_send(
        #         self.groupname,
        #         {
        #             'type': 'deprocessing2',
        #             'value': val2
        #         }
        #     )
        # else:pass

        # print('>>>>>', text_data)
        # pass

