'''Wrappers for interacting with tubes.'''
import os

class Tube:
    '''Object for interacting with tubes.'''
    def __init__(self, server):
        '''Takes a string containing a server name, e.g. chat.freenode.net, and
        gets the correct filenames for tubes' named pipes for that server.
        '''
        self.incoming = os.path.join('/tmp', '{}.in'.format(server))
        self.outgoing = os.path.join('/tmp', '{}.out'.format(server))


    def identify(self, nick, gecos):
        '''Identify ourselves to the ircd.'''
        with open(self.outgoing, 'w', encoding='utf-8') as send:
            send.write('NICK {}\r\n'.format(nick))
            send.write('USER {} * 8 :{}\r\n'.format(nick, gecos))


    def join(self, channel):
        '''Join a channel.'''
        with open(self.outgoing, 'w', encoding='utf-8') as send:
            send.write('JOIN {}\r\n'.format(channel))


    def notice(self, message, channel):
        '''Send a notice.'''
        with open(self.outgoing, 'w', encoding='utf-8') as send:
            send.write('NOTICE {} :{}\r\n'.format(channel, message))


    def privmsg(self, message, channel):
        '''Send a message.'''
        if message[:7] == '\x01ACTION':
            with open(self.outgoing, 'w', encoding='utf-8') as send:
                sanitised = ''.join(c for c in message if c.isprintable())
                send.write('PRIVMSG {} :\x01{}\x01\r\n'.format(channel, sanitised))
        else:
            with open(self.outgoing, 'w', encoding='utf-8') as send:
                sanitised = message.replace('\n', ' ',).replace('\r', '')
                send.write('PRIVMSG {} :{}\r\n'.format(channel, sanitised))


    def pong(self, reply):
        '''Reply to a ping.'''
        with open(self.outgoing, 'w', encoding='utf-8') as send:
            send.write('PONG {0}\r\n'.format(reply))
