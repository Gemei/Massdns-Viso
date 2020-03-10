import subprocess,sys
from Util import *

class Massdns_Scanner:

    def __init__(self, amass_file):
        self.RESOLVERS_PATH = "/usr/share/wordlists/massdns/resolvers.txt" #Change this
        self.list_of_domains = amass_file

    def exec_and_readlines(self, cmd, domains):

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        return stdout

    def do_scan(self):
        massdns_cmd = [
            'massdns',
            '-s', '15000',
            '-t', 'A',
            '-o', 'J',
            '-r', self.RESOLVERS_PATH,
            '--flush', self.list_of_domains
        ]

        return self.exec_and_readlines(massdns_cmd, self.list_of_domains)