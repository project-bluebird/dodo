from .create_aircraft import create_aircraft
from .utils import ping_bluebird


class PyDodo:

	def __init__(self):
		print('PyDodo constructed!')

	def create_aircraft_test(self):
		create_aircraft('TST1001', 'B744', 55.945336, -3.187299, 123.45, None, 'FL160', 250.25)

	def ping_test(self):
		resp = ping_bluebird()
		print('Ping: {}'.format('pong!' if resp else 'nope!'))
