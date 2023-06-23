"""файл для запуска серверного приложения в цикле"""
from argparse import ArgumentParser
from asyncio import get_event_loop, set_event_loop

from config import DB_PATH, PORT
from utils.proto import ChatServerProtocol
from ui.windows import ServerMonitorWindow

from quamash import QEventLoop
from PyQt5.QtWidgets import QApplication
from sys import argv


class ConsoleServerApp:
    """Console server"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()
        loop = get_event_loop()

        self.ins = ChatServerProtocol(self.db_path, connections, users)

        coro = loop.create_server(lambda: self.ins, self.args["addr"],
                                  self.args["port"])
        server = loop.run_until_complete(coro)

        print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


class GuiServerApp:
    """Gui server"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()

        self.ins = ChatServerProtocol(self.db_path, connections, users)

        app = QApplication(argv)
        loop = QEventLoop(app)
        set_event_loop(loop)

        wnd = ServerMonitorWindow(server_instance=self.ins, parsed_args=self.args)
        wnd.show()

        with loop:
            coro = loop.create_server(lambda: self.ins,
                                      self.args["addr"], self.args["port"])
            server = loop.run_until_complete(coro)

            print('Serving on {}: {}'.format(*server.sockets[0].getsockname()))
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


def parse_and_run():
    def parse_args():
        parser = ArgumentParser(description="Server settings")
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=PORT, type=int)
        parser.add_argument('--nogui', action='store_true')
        return vars(parser.parse_args())

    args = parse_args()

    if args['nogui']:
        a = ConsoleServerApp(args, DB_PATH)
        a.main()
    else:
        a = GuiServerApp(args, DB_PATH)
        a.main()


if __name__ == '__main__':
    parse_and_run()
