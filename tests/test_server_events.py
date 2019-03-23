import pytest
from multidict import MultiDict

from grpclib.events import listen, RecvRequest, RecvMessage, SendMessage
from grpclib.testing import ChannelFor

from dummy_pb2 import DummyRequest, DummyReply
from dummy_grpc import DummyServiceStub
from test_functional import DummyService


async def _test(event_type):
    service = DummyService()
    events = []

    async def callback(event_):
        events.append(event_)

    channel_for = ChannelFor([service])
    async with channel_for as channel:
        server = channel_for._server

        listen(server, event_type, callback)
        stub = DummyServiceStub(channel)
        reply = await stub.UnaryUnary(DummyRequest(value='ping'),
                                      timeout=1,
                                      metadata={'foo': 'bar'})
        assert reply == DummyReply(value='pong')

    event, = events
    return event


@pytest.mark.asyncio
async def test_recv_request():
    event = await _test(RecvRequest)
    assert event.metadata == MultiDict({'foo': 'bar'})
    assert event.method_name == '/dummy.DummyService/UnaryUnary'
    assert event.deadline.time_remaining() > 0
    assert event.content_type == 'application/grpc+proto'


@pytest.mark.asyncio
async def test_recv_message():
    event = await _test(RecvMessage)
    assert event.message == DummyRequest(value='ping')


@pytest.mark.asyncio
async def test_send_message():
    event = await _test(SendMessage)
    assert event.message == DummyReply(value='pong')