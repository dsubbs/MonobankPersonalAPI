
from pythonjsonlogger.jsonlogger import JsonFormatter


class CustomFormatter(JsonFormatter):

    def add_fields(self, log_record, record, message_dict):
        super(CustomFormatter, self).add_fields(log_record, record, message_dict)

        if log_record.get('levelname'):
            log_record['level'] = log_record['levelname'].upper()
            log_record.pop('levelname')

        module = log_record.get('module')
        message = log_record.get('message')
        if module and message:
            module = module.capitalize()
            log_record['message'] = module + ': ' + message
