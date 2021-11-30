import sys
import time
import platform
import asyncio
import logging 
from hashlib import md5
import os

from bleak import BleakClient, BleakScanner, BleakError

from display import new_media
from helpers import AMS_Helper

media_track_info = [None,None,None]
last_index = -1
last_query = None

logger = logging.getLogger(__name__)

ams_helper = AMS_Helper()

SERVICE_UUID = "89D3502B-0F36-433A-8EF4-C502AD55F8DC"
CHARACTERISTIC_UUID = "2F7CABCE-808D-411F-9A0C-BB92BA96C102"
ADDRESS = (
    ams_helper.get_device()[0]
)


async def run_ble_client(address: str, char_uuid: str, queue: asyncio.Queue):

    async def callback_handler(sender, data):
        await queue.put((time.time(), data))

    disconnected_event = asyncio.Event()
    
    def disconnected_callback(client):
        logger.info("Disconnected!")
        disconnected_event.set()

    while True:
        logger.info("Connecting...")

        try:
            async with BleakClient(address, disconnected_callback=disconnected_callback) as client:
                logger.info(f"Connected: {client.is_connected}")
                await client.start_notify(char_uuid, callback_handler)
                write_value = bytearray([0x02, 0x02, 0x00, 0x01])
                await client.write_gatt_char(char_uuid, write_value)
                await disconnected_event.wait()
                # await client.stop_notify(char_uuid)
                await queue.put((time.time(), None))

        except BleakError:
            await asyncio.sleep(1.0)

        disconnected_event.clear()


async def run_queue_consumer(queue: asyncio.Queue):
    while True:
        try:
            # get data from queue
            epoch, data = await asyncio.wait_for(queue.get(), timeout=10.0)
            if data is None:
                logger.info(
                    "Got message from client about disconnection."
                )
                # break
            else:
                logger.info(f"Received callback data via async queue at {epoch}: {data}")

            # process data 
            global media_track_info
            global last_index 
            global last_query
            if data[1] == 2:
                
                query = media_track_info[1] + " By " + media_track_info[0]
                if last_query != query:
                    last_query = query
                    media_track_info[data[1]] = bytes(data[3:]).decode("UTF-8")
                    new_media(*media_track_info)
                    

            index = data[1]
            if index < 3:
                value = bytes(data[3:]).decode("UTF-8")
                media_track_info[index] = value 

            last_index = -1

        except Exception as e:
            logger.info("Error occuered! {}".format(e))




async def main(address: str, char_uuid: str):
    queue = asyncio.Queue()
    client_task = run_ble_client(address, char_uuid, queue)
    consumer_task = run_queue_consumer(queue)
    await asyncio.gather(client_task, consumer_task)
    logger.info("Main method done.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(
        main(
            sys.argv[1] if len(sys.argv) > 1 else ADDRESS,
            sys.argv[2] if len(sys.argv) > 2 else CHARACTERISTIC_UUID,
        )
    )