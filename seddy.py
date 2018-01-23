#!/usr/bin/python3
# See the LICENSE file for licensing information
import re

nick = 'seddy'
server = 'chat.freenode.net'
channel = '#example'
gecos = 'A text processing bot'

receive = '/tmp/{0}.in'.format(server)
send = '/tmp/{0}.out'.format(server)

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
	
def msg_replace(find, replace, msg, f, n=1):
    try:
        if msg[:7] == '\x01ACTION':
            res = '\x01ACTION {0}'.format(re.sub(find, replace, msg[8:], count=n, flags=f))
        else:
            res = re.sub(find, replace, msg, count=n, flags=f)
    except:
        return False
    return res

def seddy(sed, history, parser):
    f = 0
    regex = parser.split(sed)

    if len(regex) < 4:
         return False
    if 'i' in regex[3]:
        f |= re.I
    try:
        msg = history.find(regex[1], f)
    except:
        return False
    if "g" in regex[3]:
        res = msg_replace(regex[1], regex[2], msg, 0, f)
    else:
        res = msg_replace(regex[1], regex[2], msg, 1, f)
    if res:
        res = res.replace('\0', re.search(regex[1], msg, f).group(0))
    return res

def notice(msg, channel):
    with open(send, 'w', encoding='utf-8') as g:
        g.write('NOTICE ' + channel + ' :' + msg + '\r\n')

def privmsg(msg, channel):
    if msg[:7] == '\x01ACTION':
        with open(send, 'w', encoding='utf-8') as g:
            g.write('PRIVMSG ' + channel + ' :' + '\x01' +
                    ''.join(c for c in msg if c.isprintable()) + '\x01\r\n')
    else:
        with open(send, 'w', encoding='utf-8') as g:
            g.write('PRIVMSG ' + channel + ' :' + 
                    msg.replace('\n', ' ',).replace('\r', '') + '\r\n')

if __name__ == "__main__":
    history = Queue(48)

    with open(send, 'w', encoding='utf-8') as f:
       f.write('NICK ' + nick + '\r\n')
       f.write('USER ' + nick + ' * 8 :' + gecos + '\r\n')
       sleep(5)
       f.write('JOIN ' + channel + '\r\n')

    with open(receive, 'r', encoding='utf-8') as f:
        for line in f:
            if 'PING' in line:
                with open(send, 'w', encoding='utf-8') as g:
                    g.write('PONG {0}\r\n'.format(ping.split(line)[1]))
                continue

            m = parse_msg.match(line)
            try:
                channel = m.group(1)
                msg = m.group(2)
            except:
                continue

            if history.full():
                history.dequeue()
            if 'PRIVMSG' in line and not is_sed.match(msg):
                history.enqueue(msg)

            if '.bots' in msg[:5] or '.bot ' + nick in msg[:5 + len(nick)]:
                notice("I was written to correct your mistakes.")
       	    if '.source ' + nick in msg[:8 + len(nick)]:
                notice('[Python] https://github.com/sys-fs/seddy')
            elif is_sed.match(msg):
                res = seddy(msg, history)
                if res:
                    privmsg(re.sub('\\\\/', '/', foo))
