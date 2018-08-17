from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop

import factory


def main():
    container = WSGIContainer(
        factory.create_app('lafeeclotilde_api', 'LAFEECLOTILDE_API_SETTINGS')
    )
    server = Application(
        [
            (r'.*', FallbackHandler, dict(fallback=container))
        ],
        autoreload=True
    )
    server.listen(6101)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
