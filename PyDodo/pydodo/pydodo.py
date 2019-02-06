from .create_aircraft import create_aircraft
from .utils import ping_bluebird


class PyDodo:

	def __init__(self):
		print('PyDodo constructed!')

	def create_test(self):
		create_aircraft('whee')

	def ping_test(self):
		resp = ping_bluebird()
		print('Ping: {}'.format('pong!' if resp else 'nope!'))
