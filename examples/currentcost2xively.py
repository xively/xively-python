import xively
import datetime
import sys
import time
import xml.etree.ElementTree as etree

XIVELY_API_KEY = "YOUR_API_KEY"
XIVELY_FEED_ID = 12345


def read_data(stream):
    for data in stream:
        if data == '\n':
            continue
        try:
            msg = etree.fromstring(data)
        except ET.ParseError:
            print("Error parsing data: '{}'".format(data), end='',
                  file=sys.stderr)
            continue
        date = msg.find('./date')
        hr = int(date.findtext('./hr'))
        min = int(date.findtext('./min'))
        sec = int(date.findtext('./sec'))
        watts = int(msg.findtext('.//watts'))
        tmpr = float(msg.findtext('./tmpr'))
        yield datetime.time(hr, min, sec), watts, tmpr


def main(device='/dev/ttyUSB0'):
    api = xively.XivelyAPIClient(XIVELY_API_KEY)
    feed = api.feeds.get(XIVELY_FEED_ID)
    for at, watts, tmpr in read_data(open(device, errors='ignore')):
        now = datetime.datetime.utcnow()
        feed.datastreams = [
            xively.Datastream(id='tmpr', current_value=tmpr, at=now),
            xively.Datastream(id='watts', current_value=watts, at=now),
        ]
        feed.update()
        print(at, watts, tmpr)


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        main(*args)
    except KeyboardInterrupt:
        pass
