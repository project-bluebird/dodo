from .create_aircraft import create_aircraft
from .reset_simulation import reset_simulation
from .aircraft_position import aircraft_position
from .utils import ping_bluebird


class PyDodo:

	def __init__(self):
		print('PyDodo constructed!')

	def create_aircraft_test(self):
		create_aircraft('TST1001', 'B744', 55.945336, -3.187299, 123.45, None, 160, 250.25)

	def reset_simulation_test(self):
		print("Reset simulation successful: {0}".format(reset_simulation()))

	def aircraft_position_test(self):
		print(aircraft_position())
		print(aircraft_position("all"))
		print(aircraft_position("TST1001"))
		print(aircraft_position("TST2002"))

	def ping_test(self):
		resp = ping_bluebird()
		print('Ping: {}'.format('pong!' if resp else 'nope!'))
