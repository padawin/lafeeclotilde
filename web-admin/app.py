from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop

import factory
import socket_handler


def main():
    container = WSGIContainer(factory.create_app())
    server = Application(
        [
            (r'/websocket/', socket_handler.WebSocket),
            (r'.*', FallbackHandler, dict(fallback=container))
        ],
        autoreload=True
    )
    server.listen(6100)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
