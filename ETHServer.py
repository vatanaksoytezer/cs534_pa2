import Pyro4
from MyBlockChain import MyBlockChain

ETH = MyBlockChain("ETH")
daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(ETH)   # register bitcoin as a Pyro object
ns.register("ETH", uri)   # register the object with a name in the name server

print("ETH Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls

# ! RUN python -m Pyro4.naming
