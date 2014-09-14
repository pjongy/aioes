import asyncio
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError


class TestSnapshot(unittest.TestCase):

    def setUp(self):
        self._index = 'elastic_search'
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Elasticsearch([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(self.cl.close)
        try:
            self.loop.run_until_complete(
                self.cl.delete(self._index, refresh=True))
        except NotFoundError:
            pass

    def tearDown(self):
        self.loop.close()

    def test_status(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.snapshot.status()
            self.assertEqual({'snapshots': []}, ret)

        self.loop.run_until_complete(go())
