from notifier.client.client import NotifyClient

class Notifier(object):
    __services = []

    def register(self, service):
        if not isinstance(service, NotifyClient):
            raise TypeError("service not implement NotifyClient")

        self.__services.append(service)

    def send(self, msg):
        print("sending... [%s]" % msg)

        for _, service in enumerate(self.__services):
            service.send(msg)


