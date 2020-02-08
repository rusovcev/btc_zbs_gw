"""
Bitcoin Gateway
"""
import gevent.monkey
gevent.monkey.patch_all()

from zbs_bitcoin_gateway import BitcoinGateway 
# from waves_litecoin_gateway import LitecoinGateway

file = open("config.cfg", "r")

gateway = BitcoinGateway.from_config_file(file.read())

gateway.run()
