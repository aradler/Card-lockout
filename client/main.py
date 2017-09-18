import requests
import yaml


def runLoop( config ):
	"""
	Runs indefinitely. On user input (card swipe), will gather the card number,
	send it to the server configured, and if it has been authorized, open the
	relay with a GPIO call.
	"""
	while True:
		swipe = input()

		cardNumber = swipe
		print( 'The last input was ' + cardNumber )

		try:
			res = requestAuthorization( cardNumber, config )

			if res['isAuthorized']:
				# open the relay here
				print( "Authorized!" )

			else:
				print( "Not authorized!" )

		except requests.exceptions.Timeout:
			print( "Server timeout!" )
			continue




def requestAuthorization( cardNumber, config ):
	url = 'http://' + str( config['serverAddress'] ) + ':' + str( config['serverPort'] )
	path = '/users/checkAuthorization'

	req = requests.get( url + path, {
		'cardNumber': cardNumber,
		'machineID': config['machineID'],
		'machineType': config['machineType']
	}, timeout=config['timeout'] )

	return req.json()


if __name__ == '__main__':
	# read and return a yaml file (called 'config.yaml' by default) and give it
	# back as a dictionary
	with open( 'config.yaml' ) as f:
		config = yaml.load( f )

	# run the main loop
	runLoop( config )
