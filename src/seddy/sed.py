'''Core functionality of seddy.'''

import re

def replacer(find, replace, message, flags, count=1):
    try:
        if message[:7] == '\x01ACTION':
            tmp = re.sub(find, replace, message[8:], flags=flags,
                         count=count)
            replaced = '\x01ACTION {}'.format(tmp)

        else:
            replaced = re.sub(find, replace, message, flags=flags, count=count, )
    except:
        return False

    if '\0' in message:
        whole_match = re.search(find, message, flags).group(0)
        replaced = replaced.replace('\0', whole_match)

    return replaced


def seddy(sed, history, parser):
    f = 0
    regex = parser.split(sed)

    if len(regex) < 4:
        return False

    find = regex[1]
    replace = regex[2]
    flags = regex[3]

    if 'i' in flags:
        f |= re.I

    try:
        message = history.find(find, f)
    except:
        return False


    if 'g' in flags:
        replaced = replacer(find, replace, message, f, count=0)
    else:
        replaced = replacer(find, replace, message, f)

    return replaced
