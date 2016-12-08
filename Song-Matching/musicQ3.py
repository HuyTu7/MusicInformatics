__author__ = 'Huy Tu'
# 4/14/2015
import json
import pickle
import os
import numpy

import musicD1 as dict

DATABASE = "hash_dict2.p"
Q_DIRECTORY = "queries/"

DEBUG_DATABASE = True
hash_dictionary = {}

def query(q):
	query_matrix, fs = dict.get_matrix(Q_DIRECTORY + q)
	#song, 5512, 2048
	print(query_matrix) 
	print(query_matrix.shape)
	query_hashes = dict.get_hashes(query_matrix)
	
	min_ber = 1
	best_match = None
	
	for i in range(len(query_hashes)):
		jSH = similar_hashes(query_hashes[i])
		for j in range(len(jSH)):
			if jSH[j] not in hash_dictionary["lut"]:
				continue
			for md5, offset in hash_dictionary["lut"][jSH[j]]:
				query_print = query_hashes
				match_print = hash_dictionary["songs"][md5]["hashes"]
				ber = bit_error_rate(query_print, match_print, int(offset))
				if ber < min_ber:
					min_ber = ber
					best_match = (hash_dictionary["songs"][md5]["name"], offset)
	return best_match


def bit_error_rate(query_print, match_print, offset):
	match_print = match_print[offset: offset + 30]
	if len(match_print) < 30:
		return 1
	errors = 0.0
	total = len(match_print) * 32.0
	for i in range(len(match_print)):
		if (int(query_print[i]) ^ int(match_print[i])) != 0:
			errors += 1
	return errors/total


def similar_hashes(h):
	variances = numpy.zeros(33)
	variances[0] = int(h)
	for i in range(32):
		binary = 2**i
		variances[i+1] = int(h) ^ binary
	return variances


def load_database():
	global hash_dictionary
	hash_dictionary = pickle.load(open(DATABASE, "rb"))
	print('Database contains %d unique hashes.' % len(hash_dictionary['lut'].keys()))

def main():
	load_database()
	queries = os.listdir(Q_DIRECTORY)
	for q in queries:
		match = query(q)
		print("Query: %s\tSong:%s from offset %d" % (q, match[0], match[1]))

if __name__ == "__main__":
	main()
