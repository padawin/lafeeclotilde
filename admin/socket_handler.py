import json
import logging
from tornado.websocket import WebSocketHandler


class WebSocket(WebSocketHandler):
    def open(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("Socket opened")

    def on_message(self, message):
        return

    def on_close(self):
        self._logger.info("Socket closed")
