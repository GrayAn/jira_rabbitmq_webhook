from asyncio import get_event_loop, AbstractEventLoop
from json import loads
from logging import getLogger

from aiohttp import web

from .config import load_config
from .errors import JRWException
from .amqp import AMQPConnection


class JRWApplication:
    def __init__(self, cfg_path: str, *, loop: AbstractEventLoop):
        self.cfg_path = cfg_path

        cfg = self.get_config()

        self.app = web.Application(loop=loop)
        self.app.add_routes([web.post(cfg['web']['url'], self.webhook)])

        self.default_queue = cfg['amqp']['default_queue']
        self.queues = cfg['amqp']['custom_queues'] or {}
        self.amqp = AMQPConnection(host=cfg['amqp']['host'], port=cfg['amqp']['port'],
                                   login=cfg['amqp']['login'], password=cfg['amqp']['password'],
                                   virtualhost=cfg['amqp']['virtualhost'], ssl=cfg['amqp']['ssl'],
                                   timeout=cfg['amqp']['timeout'], loop=loop)

        self.app.on_startup.append(self._startup)
        self.app.on_shutdown.append(self._shutdown)

    def get_config(self):
        return load_config(self.cfg_path)

    async def _startup(self):
        """Connecting to the RabbitMQ instance"""
        queues = set(self.queues.values())
        queues.add(self.default_queue)

        channel = await self.amqp.get_channel()
        for queue in queues:
            await channel.queue_declare(queue, durable=True)

    async def _shutdown(self):
        """Disconnecting from the RabbitMQ instance"""
        await self.amqp.shutdown()

    async def webhook(self, request: web.Request) -> web.Response:
        """Getting HTTP requests and sending their content to the RabbitMQ instance"""
        try:
            channel = await self.amqp.get_channel()
        except JRWException as e:
            getLogger('jrw').error(str(e))
            return web.Response()

        content = await request.content.read()
        data = loads(content)
        event = data['webhookEvent']
        queue = self.queues.get(event, self.default_queue)
        await channel.publish(content, '', queue, {'delivery_mode': 2})

        return web.Response()

    def __call__(self):
        return self.app()


def get_application(cfg_path: str) -> JRWApplication:
    """Application initialization"""
    loop = get_event_loop()

    app = JRWApplication(cfg_path, loop=loop)

    return app
