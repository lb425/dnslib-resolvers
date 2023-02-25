!/usr/bin/python3

###Based on DNSlib 'shellResolver.py;

# -*- coding: utf-8 -*-


from __future__ import print_function

try:
  from subprocess import getoutput
except ImportError:
  from commands import getoutput

from dnslib import RR,QTYPE,RCODE,TXT,parse_time
from dnslib.label import DNSLabel
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger

debug=False

class RedisResolver(BaseResolver):
  def __init__(self):

    import redis

    self.r = redis.Redis(
      host='192.',
      port=49153)

  def resolve(self,request,handler):
    reply = request.reply()
    qname = str(request.q.qname)
    if debug:
      print(qname)
#    cmd = self.routes.get(DNSLabel(qname))
#    print(cmd)
    data=self.r.get(qname)
    if data is not None:
      ttl=self.r.ttl(qname)
      output = data
      reply.add_answer(RR(qname,QTYPE.TXT,ttl=ttl,
                                rdata=TXT(output[:254])))
    else:
      reply.header.rcode = RCODE.NXDOMAIN
    return reply

if __name__ == '__main__':

  import sys,time
  argAddress = '127.0.0.1'
  argAddress = '192.'
  argAddress = '0.0.0.0'
  argPort = 53
  resolver = RedisResolver()
  logger = DNSLogger("/dev/null",prefix="B")

  if debug:
    print("Starting Shell Resolver (%s:%d) [%s]" % (
                        argAddress or "*",
                        argPort,
                        "UDP"))


#  if args.udplen:
#    DNSHandler.udplen = args.udplen

  udp_server = DNSServer(resolver,
                           port=argPort,
                           address=argAddress,
                           logger=logger)
  udp_server.start_thread()


  while udp_server.isAlive():
    time.sleep(1)
