import argparse
import re
import subprocess
import sys


class Conversation(object):
    def __init__(self, id, src_ip, src_port, dst_ip, dst_port, tbytes, duration):
        self.id = id
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.tbytes = tbytes
        self.duration = duration

    @classmethod
    def create(cls, c):
        _c = [x for x in c.split(" ") if not x == '']
        convo_dict = dict(id=i, src_ip=_c[0].split(":")[0], src_port=_c[0].split(":")[1],
                          dst_ip=_c[2].split(":")[0], dst_port=_c[2].split(":")[1],
                          tbytes=_c[8], duration=_c[10])
        return Conversation(**convo_dict)

    def follow(self):
        f_command = "tshark -nqr {} -z follow,{},ascii,{},{}".format(args.pcap, args.protocol, ":".join([self.src_ip, self.src_port]), ":".join([self.dst_ip, self.dst_port]))
        f_process = subprocess.Popen(f_command, shell=True, stdout=subprocess.PIPE)
        f_out, f_err = f_process.communicate()
        return f_out

    def __str__(self):
        return "{}) {}:{} <-> {}:{} ({} Total bytes, Duration: {})".format(self.id, self.src_ip, self.src_port,
                                                                          self.dst_ip, self.dst_port,
                                                                          self.tbytes, self.duration)

def input_validation(i):
    """Basic input validation."""
    if re.findall(r'[^A-Za-z0-9_.]',i):
        return False
    else:
        return True


def has_ip(l):
    ip_re = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
    if ip_re.search(l):
        return True
    else:
        return False


def menu():
    print("Which conversations would you like to follow?: \n{}".format("\n".join([c.__str__() for c in conversations.values()])))
    user_in = raw_input("Your selection: ")
    try:
        print(conversations[int(user_in)].follow())
    except KeyError:
        print("You didn't pick a valid conversation.")
        menu()
    except:
        print("Something unexpected went wrong, killing program.")
        sys.exit(1)
    user_continue = raw_input("Would you like to see another conversation? (y/N): ")
    if user_continue.lower() == 'y':
        menu()
    else:
        sys.exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("pcap", help="The PCAP file you want conversations from.")
parser.add_argument("--protocol", "-p", choices=("udp", "tcp"), default="tcp", help="The protocol to follow, choose TCP or UDP. Default is TCP")
args = parser.parse_args()
assert input_validation(args.pcap), "This program only allows filenames with Alphanums, periods and underscores."
t_command = "tshark -nqr {} -z conv,{}".format(args.pcap, args.protocol)
process = subprocess.Popen(t_command, shell=True, stdout=subprocess.PIPE)
out, err = process.communicate()
i = 0
convos = [x for x in [y for y in out.split("\n") if len(y) > 0] if x[0].isdigit()]
conversations = dict()
for conv in convos:
    if has_ip(conv):
        c = Conversation.create(conv)
        conversations[c.id] = c
        i += 1
menu()