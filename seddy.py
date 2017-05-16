#!/usr/bin/python3
# See the LICENSE file for licensing information
import re

nick = 'seddy'
server = 'chat.freenode.net'
channel = '#example'
gecos = 'A text processing bot'

receive = open('/tmp/' + server + '.in', 'r')
send = open('/tmp/' + server + '.out', 'w')

parse_msg = re.compile(channel + ' :(.*)')
parse_sed = re.compile('(?<!\\\\)/')
is_sed = re.compile('^s/.*/.*')

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

    def find(self, s, flags=0):
        i = self.tail-1
        while True:
            if i == -1:
                i = self.size-1
            if re.search(s, self.data[i], flags):
                return self.data[i]
            i -= 1
            if i == self.tail-1 or self.data[i] is None:
                return False

def seddy(sed, history):
    f = 0
    regex = parse_sed.split(sed)

    if len(regex) < 4:
	return False
    if 'i' in regex[3]:
        f |= re.I
    try:
        msg = history.find(regex[1], f)
    except:
        msg = False
    if msg == False:
        return False
    if "g" in regex[3]:
        try:
            res = re.sub(regex[1], regex[2], msg, flags=f)
        except:
            res = False
    else:
        try:
            res = re.sub(regex[1], regex[2], msg, 1, f)
        except:
            res = False
    return res

def notice(msg):
    send.write('NOTICE ' + channel + ' :' + msg + '\r\n')
    send.flush()

def privmsg(msg):
    if msg[:7] == '\x01ACTION':
        send.write('PRIVMSG ' + channel + ' :' + '\x01' +
                   ''.join(c for c in msg if c.isprintable()) + '\x01\r\n')
    else:
        send.write('PRIVMSG ' + channel + ' :' +
                   ''.join(c for c in msg if c.isprintable()) + '\r\n')
    send.flush()

if __name__ == "__main__":
    history = Queue(48)

    send.write('NICK ' + nick + '\r\n')
    send.flush()
    send.write('USER ' + nick + ' * 8 :' + gecos + '\r\n')
    send.flush()
    send.write('JOIN ' + channel + '\r\n')
    send.flush()

    for line in receive:
        msg = parse_msg.search(line)
        if msg is None:
	    if 'PING' in line:
                send.write('PONG\r\n')
                send.flush()
            continue
        else:
            msg = msg.group(1)

        if history.full():
            history.dequeue()
        if 'PRIVMSG' in line and not is_sed.match(msg):
            history.enqueue(msg)

        if '.bots' in msg[:5] or '.bot ' + nick in msg[:5 + len(nick)]:
            notice("I was written to correct your mistakes.")
	if '.source ' + nick in msg[:8 + len(nick)]:
            notice('[Python] https://github.com/sys-fs/seddy')
        elif is_sed.match(msg):
            foo = seddy(msg,history)
            if foo != False:
                privmsg(re.sub('\\\\/', '/', foo))
