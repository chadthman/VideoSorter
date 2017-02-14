#!/usr/bin/python

import sys
import getopt
import os
import re

USAGE_METHOD = 'VideoSorter.py -d <directory>'
FILE_PATTERN = re.compile("^.*(\.mkv|\.m4v|\.avi)$", re.IGNORECASE)

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hd:o:",["dir=","outdir="])
	except getopt.GetoptError:
		print USAGE_METHOD
		sys.exit(2)
	if not opts:
		print USAGE_METHOD
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print USAGE_METHOD
			sys.exit()
		elif opt in ("-d", "--dir"):
			inputdir = arg
		elif opt in ("-o", "--outdir"):
			outputdir = arg
	if not inputdir or not outputdir:
		print USAGE_METHOD
		sys.exit()
	print 'Scan dir is "', inputdir
	print 'Output dir is "', outputdir

	for dirname, dirnames, filenames in os.walk(inputdir):
		for filename in filenames:
			if FILE_PATTERN.match(filename):
				try:
					season = re.search("(S|s)[0-9]?[0-9](E|e)", filename).group(0)[1:][:-1]
					episode = re.search("(E|e)[0-9]?[0-9]", filename).group(0)[1:]
					showName = re.search(".+?(?=(S|s)[0-9]?[0-9](E|e))", filename).group(0).replace(".", " ").strip()
					extension = filename.split(".")[-1]
					newFileName = showName + " - " + "S" + season.zfill(2) + "E" + episode.zfill(2) + "." + extension
					newDirName = "/" + showName + "/Season " + str(int(season)) + "/"
					if (not os.path.exists(outputdir + newDirName)):
						os.makedirs(outputdir + newDirName)
					os.rename(os.path.join(dirname, filename), outputdir + newDirName + newFileName)
				except AttributeError:
					continue
				print(newFileName)
				print(os.path.join(dirname, filename))

		if '.*' in dirnames:
			# don't go into any .* directories.
			dirnames.remove('.*')
		if 'Sample' in dirnames: 
			dirnames.remove('Sample')

if __name__ == "__main__":
	main(sys.argv[1:])

