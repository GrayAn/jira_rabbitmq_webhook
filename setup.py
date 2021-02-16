#!/usr/bin/env python

from setuptools import setup

from jira_rabbitmq_webhook import __version__

with open('README.rst', 'r') as f:
    readme = f.read()


setup(
    name='jira_rabbitmq_webhook',
    version=__version__,
    url='https://github.com/GrayAn/jira_rabbitmq_webhook',
    license='MIT',
    author='Sergey Shubin',
    author_email='greyan@gmail.com',
    description='A microservice for retranslating Jira webhooks to a RabbitMQ server',
    long_description=readme,
    packages=['jira_rabbitmq_webhook'],
    data_files=[
        ('config', ('config/jira_rabbitmq_webhook.json.example',)),
    ],
    python_requires='>=3.5',
    install_requires=[
        'aioamqp<1.0',
        'aiohttp>=3.0,<4.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Bug Tracking',
    ],
)
