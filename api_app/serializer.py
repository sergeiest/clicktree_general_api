from tastypie.serializers import Serializer
from datetime import datetime
import logging
import json
import pytz

class CustomJSONSerializer(Serializer):
    def from_json(self, content):
        #logging.info(content)
        data = json.loads(content)

        if 'time' in data:
                data['time'] = datetime.fromtimestamp(float(data['time'])/1000.0, tz=pytz.utc)
        logging.info("after loading time to data in from_json")
        if 'headers' in data:
            if 'host' in data['headers']:
                    data['host'] = data['headers']['host'] if len(data['headers']['host']) < 200 else data['headers']['host'][:200]
            if 'useragent' in data['headers']:
                    data['useragent'] = data['headers']['useragent'] if len(data['headers']['useragent']) < 200 else data['headers']['useragent'][:200]
            if 'language' in data['headers']:
                    data['lang'] = data['headers']['language']
            if 'referer' in data['headers']:
                    data['referer'] = data['headers']['referer'] if len(data['headers']['referer']) < 200 else data['headers']['referer'][:200]
            if 'encoding' in data['headers']:
                    data['encode'] = data['headers']['encoding']
       # logging.info("finish from_json")

        return data