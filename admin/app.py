import os

from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop

import factory
import socket_handler


def main():
    project_path = os.path.dirname(os.path.realpath(__file__))
    container = WSGIContainer(
        factory.create_app(
            'lafeeclotilde_admin',
            'LAFEECLOTILDE_ADMIN_SETTINGS',
            template_folder=f'/{project_path}/templates'
        )
    )
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
