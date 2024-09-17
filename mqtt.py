"""Publish state via MQTT."""

import logging
from dotenv import load_dotenv
import os
import paho.mqtt.publish as publish
from paho.mqtt import client as mqtt_client

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s - %(message)s")

class Publisher():
    """A class that will take care of publishing MQTT messages.

    :param channel: The channel that the messages will be published on.
    :param server: The MQTT server messages will be sent to.
    """
    def __init__(self, channel, server):
        self.channel = channel
        self.server = os.getenv("MQTT_SERVER")
        self.port = int(os.getenv("MQTT_PORT"))
        self.client_id = "enviropi"

        self.__connect()

    def __connect(self):
        """Connect to MQTT server."""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT server.")
            else:
                logging.error("Failed to connect to MQTT server.")

        client = mqtt_client.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt_client.MQTTv311, transport="tcp")
        client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
        client.on_connect = on_connect
        client.connect(self.server, self.port, 60)
        client.loop_forever()

    def publish(self, message) -> bool:
        """Publish message to MQTT server.

        :param message: the message to publish.
        """

        try:
            publish.single(self.channel, message, hostname=self.server, client_id=self.client_id)
            return True
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")
            logging.error("Server DNS issue.")
            return False
