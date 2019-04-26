from asyncio import sleep, AbstractEventLoop, Lock
from asyncio.transports import Transport
from typing import Tuple

from aioamqp import connect, protocol
from aioamqp.channel import Channel
from aioamqp.protocol import AmqpProtocol

from .errors import JRWAMQPException


class AMQPConnection:
    """
    Handling AMQP connections: connecting and reconnecting
    to the RabbitMQ server and getting channels.
    """
    def __init__(self, host: str, port: int, login: str, password: str,
                 virtualhost: str, ssl: bool, timeout: int, *, loop: AbstractEventLoop):
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self._virtualhost = virtualhost
        self._ssl = ssl
        self._timeout = timeout
        self._loop = loop

        self._transport = None
        self._protocol = None
        self._channel = None

    async def _connect(self) -> Tuple[Transport, AmqpProtocol]:
        return await connect(host=self._host, port=self._port, login=self._login, password=self._password,
                             virtualhost=self._virtualhost, ssl=self._ssl, loop=self._loop)

    async def shutdown(self):
        """Graceful shutdown, should be called on application shutdown"""
        if self._protocol is not None:
            if self._protocol.state != protocol.CLOSED:
                await self._protocol.close()
            self._transport.close()

    async def get_protocol(self) -> AmqpProtocol:
        """Connecting to the RabbitMQ instance"""
        async with Lock():

            if self._protocol is None or self._protocol.state != protocol.OPEN:

                self._channel = None

                for i in range(self._timeout):
                    try:
                        self._transport, self._protocol = await self._connect()
                    except ConnectionRefusedError:
                        await sleep(1)
                    else:
                        break

                if self._protocol.state != protocol.OPEN:
                    raise JRWAMQPException('Timeout error: cannot connect to the MQ server')

            return self._protocol

    async def get_channel(self) -> Channel:
        """Getting RabbitMQ channel"""
        pr = await self.get_protocol()
        if self._channel is None:
            self._channel = await pr.channel()
        return self._channel
