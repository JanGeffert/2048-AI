import os
import sys
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Welcome to 2048, AI edition.')

	parser.add_argument("log", metavar="LOG")
 
	args = parser.parse_args()

	os.system("python -m http.server")
	os.system("open http://0.0.0.0:8000/replay/?log=/{}".format(args["log"]))