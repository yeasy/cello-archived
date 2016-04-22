import __future__

from ..common import get_project


class Cluster(object):
    def __init__(self, name, daemon_url):
        self.name = name
        self.daemon_url = daemon_url


if __name__ == "__main__":
    get_project(".")