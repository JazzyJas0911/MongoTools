import logging
import argparse


def argcreate():
    #ArgumentParser holds the info necessary to parse the command line into Python data types.
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

def argtut():
    parser= argparse.ArgumentParser()
    parser.add_argument("bark", help="echo the string you use here")
    args = parser.parse_args()
    print(args.bark)

def loggstuff(): 
	# create logger
	logger = logging.getLogger('Logger_Test')
	logger.setLevel(logging.DEBUG)

	# create console handler and set level to debug
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)

	# create formatter
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	# add formatter to ch
	ch.setFormatter(formatter)

	# add ch to logger
	logger.addHandler(ch)

	# 'application' code
	logger.debug('debug message')
	logger.info('info message')
	logger.warning('warn message')
	logger.error('error message')
	logger.critical('critical message')

	logger.info('Begging test loop')
#argcreate()
argtut()
