Jira RabbitMQ WebHook
=====================

This service works as a bridge between a Jira and a RabbitMQ instances:

* receives HTTP requests from the Jira server;
* sends them to the MQ server via AMQP protocol.

Installation
------------

The service requires Python 3.5 or newer.
Install and update using `pip`_.
`Gunicorn`_ is also required:

.. code-block:: text

    pip install jira_rabbitmq_webhook gunicorn

Configuration
-------------

You need to create a configuration file for the service.
Sample file can be found in ``config`` directory (it is copied to the
``config`` directory of your python environment after installation). Available settings:

* web

  * url - URL used for receiving HTTP requests from the Jira instance

* amqp

  * host - RabbitMQ host
  * port - RabbitMQ port
  * login - RabbitMQ login
  * password - RabbitMQ login
  * virtualhost - RabbitMQ virtual host to use
  * timeout - How many seconds the service tries to connect to the RabbitMQ server
  * ssl - Whether to use SSL for AMQP connection
  * default_queue - Queue to send messages to
  * custom_queues - Queues to send messages for specific events

You also need to configure Jira webhook to send requests to your jira_rabbitmq_webhook instance.
For example if your jira_rabbitmq_webhook instance is launched on the host jrw.test.com
and you configured "web"->"url" as "/webhook/" then you should set webhook address in your Jira instance
as "http://jrw.test.com/webhook/" (or "https://jrw.test.com/webhook/" if you configured SSL for it).

Running
-------

The jira_rabbitmq_webhook service can be launched with the Gunicorn:

.. code-block:: text

    gunicorn "jira_rabbitmq_webhook.application:get_application('path/to/the/jira_rabbitmq_webhook.json')" --worker-class aiohttp.GunicornWebWorker

.. _Gunicorn: https://gunicorn.org/
.. _pip: https://pip.pypa.io/en/stable/quickstart/
