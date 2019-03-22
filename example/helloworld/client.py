import asyncio

from grpclib.client import Channel

from .helloworld_pb2 import HelloRequest
from .helloworld_grpc import GreeterStub


async def main():
    loop = asyncio.get_event_loop()
    channel = Channel('127.0.0.1', 50051, loop=loop)
    # stub = GreeterStub(channel)

    # response = await stub.SayHello(HelloRequest(name='World'))
    # print(response.message)

    await channel.__connect__()
    await asyncio.sleep(12)

    channel.close()
    await channel.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
