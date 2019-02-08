import argparse

from pydodo import PyDodo, settings

if __name__ == '__main__':
	# Parse the bluebird host address from the CLI arguments
	PARSER = argparse.ArgumentParser()
	PARSER.add_argument('--bluebird_host', type=str, help='', default='0.0.0.0')
	ARGS = PARSER.parse_args()
	settings.BB_HOST = ARGS.bluebird_host

	p = PyDodo()
	p.ping_test()
	p.reset_simulation_test()
	p.create_aircraft_test()
	p.aircraft_position_test()
