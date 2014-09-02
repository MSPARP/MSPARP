#!/usr/bin/env python

import sys
import socket
import re
from dns.resolver import Resolver, NXDOMAIN, NoNameservers, Timeout, NoAnswer
from dns.query import udp
from threading import Thread

RBLS = [
    'tor.dnsbl.sectoor.de',
    #'rbl.efnetrbl.org',
    'sbl-xbl.spamhaus.org',
]


class Lookup(Thread):
    def __init__(self, host, dnslist, listed, resolver):
        Thread.__init__(self)
        self.host = host
        self.listed = listed
        self.dnslist = dnslist
        self.resolver = resolver

    def run(self):
        try:
            host_record = self.resolver.query(self.host, "A")
            if len(host_record) > 0:
                self.listed[self.dnslist]['LISTED'] = True
                self.listed[self.dnslist]['HOST'] = host_record[0].address
                text_record = self.resolver.query(self.host, "TXT")
                if len(text_record) > 0:
                    self.listed[self.dnslist]['TEXT'] = "\n".join(text_record[0].strings)
            self.listed[self.dnslist]['ERROR'] = False
        except NXDOMAIN:
            self.listed[self.dnslist]['ERROR'] = True
            self.listed[self.dnslist]['ERRORTYPE'] = NXDOMAIN
        except NoNameservers:
            self.listed[self.dnslist]['ERROR'] = True
            self.listed[self.dnslist]['ERRORTYPE'] = NoNameservers
        except Timeout:
            self.listed[self.dnslist]['ERROR'] = True
            self.listed[self.dnslist]['ERRORTYPE'] = Timeout
        except NameError:
            self.listed[self.dnslist]['ERROR'] = True
            self.listed[self.dnslist]['ERRORTYPE'] = NameError
        except NoAnswer:
            self.listed[self.dnslist]['ERROR'] = True
            self.listed[self.dnslist]['ERRORTYPE'] = NoAnswer

class RBLSearch(object):
    def __init__(self, lookup_host):
        self.lookup_host = lookup_host
        self._listed = None
        self.resolver = Resolver()
        self.resolver.timeout = 2.0
        self.resolver.lifetime = 5.0

    def search(self):
        if self._listed is not None:
            pass
        else:
            host = self.lookup_host.split(".")
            host = ".".join(list(reversed(host)))
            self._listed = {'SEARCH_HOST': self.lookup_host}
            threads = []
            for LIST in RBLS:
                self._listed[LIST] = {'LISTED': False}
                query = Lookup("%s.%s" % (host, LIST), LIST, self._listed, self.resolver)
                threads.append(query)
                query.start()
            for thread in threads:
                thread.join()
        return self._listed
    listed = property(search)

    def print_results(self):
        listed = self.listed
        print("")
        print("--- DNSBL Report for %s ---" % listed['SEARCH_HOST'])
        
        for key in listed:
            if key == 'SEARCH_HOST':
                continue
            if listed[key]['ERROR']:
                if listed[key]['ERRORTYPE'] == NXDOMAIN:
                    print("clean %s" % key)
                else:
                    print("error %s %s" % (key, listed[key]['ERRORTYPE']))
                
        for key in listed:
            if key == 'SEARCH_HOST':
                continue
            if not listed[key]['ERROR']:
                print("listed %s" % key)
                #if listed[key]['LISTED']:
                #    print("Results for %s: %s" % (key, listed[key]['LISTED']))
                #    print("  + Host information: %s" % \
                #          (listed[key]['HOST']))
                #if 'TEXT' in listed[key].keys():
                #    print("    + Additional information: %s" % \
                #          (listed[key]['TEXT']))


if __name__ == "__main__":
    # Tests!
    try:
        if len(sys.argv) > 1:
            print("Looking up: %s (please wait)" % sys.argv[1])
            ip = sys.argv[1]
            pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
            is_ip_address = pat.match(ip)
            if not is_ip_address:
                try:
                    ip = socket.gethostbyname(ip)
                    print("Hostname %s resolved to ip %s" % (sys.argv[1],ip))
                except socket.error:
                    print("IP %s can't be resolved" % ip)
                    ip = ""
            if ip:
                searcher = RBLSearch(ip)
                searcher.print_results()
        else:
            print("""Usage summary:

rblwatch <ip address to lookup> """)
    except KeyboardInterrupt:
        pass
