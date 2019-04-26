class JRWException(Exception):
    """Generic jira_rabbitmq_webhook exception"""


class JRWAMQPException(JRWException):
    """Message queue exception"""
