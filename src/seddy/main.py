# See the LICENSE file for licensing information
'''The bot itself.'''

import re
from time import sleep
from . import tubes
from . import sed

class Queue:
    size = 0
    data = []
    head = 0
    tail = 0
    count = 0

    def __init__(self, size):
        self.size = size
        self.data = [None]*size

    def enqueue(self, s):
        if not self.full():
            self.count += 1
            self.data[self.tail] = s
            self.tail = (self.tail + 1) % self.size

    def dequeue(self):
        if not self.empty():
            self.count -= 1
            s = self.data[self.head]
            self.head = (self.head + 1) % self.size
            return s

    def full(self):
        return self.size == self.count

    def empty(self):
        return self.head == self.count

    def find(self, s, f=0):
        i = self.tail-1
        while True:
            if i == -1:
                i = self.size-1
            if re.search(s, self.data[i], f):
                return self.data[i]
            i -= 1
            if i == self.tail-1 or self.data[i] is None:
                return False


def main():
    nick = 'seddy'
    server = 'lain.church'
    channel = '#sedward'
    gecos = 'A text processing bot'

    history = Queue(48)
    tube = tubes.Tube(server)
    ping = re.compile('PING :(.*)')
    parse_message = re.compile('.* PRIVMSG {} :(.*)'.format(channel))
    slash_sed = re.compile('^s/.*/.*')
    comma_sed = re.compile('^s,.*,.*')
    slash_parser = re.compile('(?<!\\\\)/')
    comma_parser = re.compile('(?<!\\\\),')

    tube.identify(nick, gecos)
    sleep(5)
    tube.join(channel)

    with open(tube.incoming, 'r', encoding='utf-8') as receive:
        for line in receive:
            if re.match(ping, line):
                tube.pong(ping.split(line)[1])
                continue

            tmp = parse_message.match(line)
            try:
                message = tmp.group(1)
            except:
                continue

            if history.full():
                history.dequeue()
            if not slash_sed.match(message) and not comma_sed.match(message):
                history.enqueue(message)

            if slash_sed.match(message):
                response = sed.seddy(message, history, slash_parser)
                if response:
                    response = re.sub('\\\\/', '/', response)
                    if history.full():
                        history.dequeue()
                    history.enqueue(response)
                    tube.privmsg(response, channel)
            elif comma_sed.match(message):
                response = sed.seddy(message, history, comma_parser)
                if response:
                    response = re.sub('\\\\,', ',', response)
                    if history.full():
                        history.dequeue()
                    history.enqueue(response)
                    tube.privmsg(response, channel)
