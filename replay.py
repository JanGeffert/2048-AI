# replay.py
# ---------------
# Starts a webserver with a visual replay of a given CSV game
# log file

import os
import sys
import argparse
import subprocess

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Welcome to 2048, AI edition.')

	parser.add_argument("log", metavar="LOG", help="The path to a csv logfile.")
	parser.add_argument("-s", "--speed", default=500, type=int, help="artifical\
 delay between turns in milliseconds")

	args = parser.parse_args()
	url = "http://0.0.0.0:8000/replay/?log={}&speed={}".format(args.log, args.speed)
	with open(os.devnull, 'w') as devnull:
		subprocess.Popen(["python","-m","http.server"], stdout=devnull, stderr=devnull)
		subprocess.Popen(["python","-m","webbrowser","-t",url], stdout=devnull, stderr=devnull)
	sys.exit(0)
