import argparse
import errno
import json
import logging
import os
import socket
import subprocess
import sys
import webbrowser


class Shell(object):
    def __init__(self):
        self.log = logging.getLogger('sshh')
        self.hosts = {}

    def load(self):
        config = json.load(open(
                '{HOME}/.sshh/config.json'.format(**os.environ)))
        for prop in config.get('files', []):
            input_path = prop['path'].format(**os.environ)
            if not os.path.isabs(input_path):
                input_path = os.path.join(os.environ.get('HOME'), '.sshh',
                                          input_path)
            try:
                with open(input_path) as input_file:
                    if prop.get('type') == 'json':
                        for node in json.load(input_file)['nodes']:
                            host = node['name']
                            if '.' not in host and prop.get('domain'):
                                host += '.' + prop['domain']
                            self.hosts[host] = node.get('ipv4')
                    else:
                        for line in input_file:
                            line = line.strip()
                            if line:
                                fields = line.split()
                                self.hosts[' '.join(fields[:-1])] = fields[-1]
            except OSError as error:
                if error.errno != errno.ENOENT:
                    raise

    def connect(self, host, address, use_exec=False):
        if ':' in address:
            return webbrowser.open(address)

        try:
            ip = socket.gethostbyname(host)
            if ip != address:
                self.log.warning(
                    'host %s resolves to different IP (%s) than expected (%s)',
                    ip, address)
            else:
                address = host  # use hostname to connect when it resolves ok
        except socket.gaierror:
            pass

        if os.environ.get('TERM') == 'screen':
            ret = subprocess.call(['screen', '-t', host.split('.')[0],
                                   'ssh', address])
            assert not ret
        else:
            if use_exec:
                os.execvp('ssh', ['ssh', address])
            else:
                return subprocess.call(['ssh', address])

    def filter(self, patterns, open_all=False, query_only=False):
        found = []
        for host, address in sorted(self.hosts.items()):
            if not patterns or all((p.lower() in host.lower())
                                   for p in patterns):
                found.append((host, address))

        for host, address in found:
            print('{0:50}  {1}'.format(host, address))
            if not query_only and (len(found) == 1 or open_all):
                self.connect(host, address, use_exec=(len(found) == 1))

    def main(self, args):
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('-a', '--all', default=False, action='store_true',
                            help='connect to all matching hosts')
        parser.add_argument('-q', '--query', default=False,
                            action='store_true', help='query only')
        parser.add_argument('pattern', nargs='*',
                            help='host filter pattern')

        arg = parser.parse_args(args)
        self.load()
        self.filter(arg.pattern, open_all=arg.all, query_only=arg.query)

    @classmethod
    def run_exit(cls):
        logging.basicConfig(level=logging.INFO)
        sys.exit(cls().main(sys.argv[1:]) or 0)


if __name__ == '__main__':
    Shell.run_exit()
