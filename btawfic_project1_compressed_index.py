# COMP90042 - Web Text and Search Analysis Project 1
# Bilal Tawfic (btawfic) 329904
"""
This module contains a set of functions that are required in creating compressed 
inverted indexes.

Included in this module are:
	- variable byte encoding functions 
 	- a function that takes the reuters corpus and creates a dictionary of 
 		terms to a postings list. 
 	- a function which takes a dictionary and converts it to a dictionary 
 		as a string.
 	- a function which takes a dictionary and a blocksize and implements
 		block storage algorithm
 	- a incomplete implementation of the SPIMI algorithm
"""

import os
from nltk.corpus import reuters
from nltk.stem.porter import PorterStemmer as stem

def remove_punct_from_word(word):
	"""
	A function that given a word returns the word without any punctuation
	"""
	punct = '`,./[]{}&!?;:$*+><()"-\'\n\t'
	new_word = []
	for char in word:
		if char not in punct and not char.isspace():
			new_word.append(char)

	
	return "".join(new_word)

def is_number(string):
	"""
	A function that given a string returns true if the string is a number
	and false if the string is not a number.
	"""
	string =  string.strip()
	try:
		float(string[0])
		return True
	except ValueError:
		return False

def vb_encode_number(n):
	"""
	A function that takes one number and returns the series
	of 8 bytes that represent it. The last set of bytes to
	represent the number begins with a '1' in the highest bit.
	"""
	bytes = []

	while (True):
		rem = n % 128
		# Get the binary representation
		binary = str(bin(rem))
		# Remove the python addition of '0b' and make it 8 bits
		binary = (binary.lstrip('0b')).zfill(8)
		bytes.insert(0, binary)
		if n < 128:
			break
		n = n / 128
	# Processing to ensure that last set of bytes begins with 1
	lastindex = len(bytes)-1
	final_byte = int(bytes[lastindex], 2)
	final_byte += 128
	# Convert back to binary
	final_byte = str(bin(final_byte))
	final_byte = (final_byte.lstrip('0b')).zfill(8)
	# Put back processed version of final byte
	bytes[lastindex] = final_byte

	return bytes

def vb_encode(numbers):
	"""
	A function that takes a list of numbers and returns
	a list of bytes that represent each number.
	"""
	bytestream = []

	for n in numbers:
		bytes = vb_encode_number(n)
		bytestream.append(bytes)

	return bytestream

def vb_decode(bytestream):
	"""
	A function that takes a list of bytes and converts them
	into a list of integers and returns the list.
	"""
	numbers = []
	n = 0

	for i in range(len(bytestream)):
		number_i_bytes = bytestream[i]
		for j in range(len(number_i_bytes)):
			byte_j = number_i_bytes[j]
			# Convert back to an int from byte
			byte_j = int(byte_j, 2)
			if (byte_j < 128):
				n = 128 * n + byte_j
			else:
				n = 128 * n + (byte_j -128)
				numbers.append(n)
				n = 0

	return numbers

def merge(doc1_filename, doc2_filename, output_filename):
	"""
	A function that is given 2 files and an output file.
	It returns the 2 given files merged in the output file.
	"""
	doc1 = open(doc1_filename, 'rb')
	try:
		doc2 = open(doc2_filename, 'rb')
	except IOError:
		doc2 = ""
	outputfile = open(output_filename, 'wb')
	i = 0
	j = 0

	doc1_termID = []
	first_byte = 0
	current_pos = 0
	byte_length = 8

	doc1.seek(current_pos)
	#doc2.seek(current_pos)

	# Get the current term in each document
	# while (doc1.read(1) != ""): # or (doc2.read(1) != ""):
	# 	doc1.seek(current_pos)
		#doc2.seek(current_pos)
		
		# doc1_termID_byte = " "

		# while doc1_termID_byte[0] != '1':
		# 	doc1_termID_byte = str(doc1.read(byte_length))
		# 	doc1_termID.append(doc1_termID_byte)

		# print doc1_termID


	# while (i < len(doc1)) and (j < len(doc2)):
	# 	# Can do this because all chars are lower case
	# 	if doc1[i] <= doc2[j]:
	# 		outputfile.write(doc1[i])
	# 		i += 1
	# 	else:
	# 		outputfile.write(doc2[j])
	# 		j += 1

	return outputfile


def spimi_invert(token_stream):
	"""
	An implementation of the single-pass in-memory indexing algorithm
	This function takes a token_stream which will be a list of tuples
	The first item in the tuple is the term and the second the docID
	i.e. [('a', 1)] - Here 'a' is the term and it is in docID 1
	"""
	dictionary = {}
	# Check for free memory
	# To do this just setting random value of j
	# And checking it is not bigger than the length of token_stream
	j = 0
	maximum_j = 10000
	block_number = 1
	if maximum_j > len(token_stream):
		maximum_j = len(token_stream)

	print "SPIMI processing block", block_number
	while (j < maximum_j):
		token = token_stream[j][0]
		if token not in dictionary:
			dictionary[token] = []
		# Add the document ID to postings list
		docID = token_stream[j][1]
		# Make sure the docID is not already listed for the term
		if docID not in dictionary[token]:
			dictionary[token].append(docID)

		# Increment j
		j += 1

		# Check to see if we have reached the maximum (run out of mem)
		if (j == maximum_j):
			# Sort the dictionary keys
			sorted_dictionary = sorted(dictionary.iterkeys())
			# Write the dictionary keys to a file
			filename = "spimiblocks/block" + str(block_number)
			block_number += 1
			dir = os.path.dirname(filename)
			if not os.path.exists(dir):
				os.makedirs(dir)
			f = open(filename, 'wb')
			for key in sorted_dictionary:
				encoded_termID = vb_encode_number(key)
				encoded_postings = vb_encode(dictionary[key])
				# Get the binary representation of termID
				for byte in encoded_termID:
					# Write the term id binary to the file
					binary = bin(int(byte)).lstrip('0b')
					f.write(binary)
					postings_length = vb_encode_number(len(dictionary[key]))
					for length_byte in postings_length:
						# Write the length of the postings list to the file
						# This is to help read information later
						length_binary = bin(int(length_byte)).lstrip('0b')
						f.write(length_binary)
					for posting in encoded_postings:
						for posting_byte in posting:
							# Write each byte to file for postings list
							posting_bianry = bin(int(posting_byte)).lstrip('0b')
							f.write(posting_bianry)

			f.close()
			# Reset dictionary
			dictionary = {}
			# Reset j and check to make sure less than token_stream size
			j = maximum_j
			maximum_j *= 2
			if maximum_j > len(token_stream):
				maximum_j = len(token_stream);
	
	# Merge the blocks together
	if (block_number == 1):
		return "spimiblocks/block1.txt"

	x = block_number-1
	outputfilenumber = 0
	while (x > 0):
		outputfilenumber += 1
		doc1 = "spimiblocks/block" + str(x)
		doc2 = "spimiblocks/block" + str(x-1)
		output_filename = "spimiblocks/outputfile" + str(outputfilenumber) 
		outputfile = merge(doc1, doc2, output_filename)
		x -= 2

def create_token_stream():
	"""
	A funtion that creates token stream based on the nltk reuters corpus
	A token stream is a list of tuples containing terms to docID
	"""
	token_stream = []
	docID = 1
	termID = 1
	print "Creating token stream..."
	for fileid in reuters.fileids('barley'):
	 	for term in reuters.words(fileid):
 			# Strip punctuatuion from the word and make lower case
 			term = remove_punct_from_word(term).lower()
 			# Check to make sure word is not "" and term is not a number
 			if len(term) > 0 and not is_number(term):
 				stemmed_term = stem().stem_word(term)
 				if stemmed_term not in terms:
 					terms[stemmed_term] = termID
 					termID += 1
 				new_token = (terms[stemmed_term], docID)
 				token_stream.append(new_token)
	 	# Add to docs dictionary mapping docID to file
	 	docs[docID] = fileid
	 	docID += 1
	return token_stream

def create_dictionary_index_reuters():
	""" 
	A function that creates a dictonary with terms as keys
	and positings lists as values for the nltk reuters corpus
	"""

	idx = {}
	docs = {}
	docID = 1
	for fileid in reuters.fileids():
	 	for word in reuters.words(fileid):
	 		if not is_number(word):
	 			# Strip punctuatuion from the word and make lower case
	 			word = remove_punct_from_word(word).lower()
	 			# Check to make sure word is not ""
	 			if len(word) > 0:
	 				# Check to see if word already is in index
	 				if word in idx:
	 					# Check to see if docID is not already present for word
	 					if docID not in idx[word]:
	 						idx[word].append(docID)
	 				# Otherwise add word and docID in array to index
	 				else:
	 					idx[word] = []
	 					idx[word].append(docID)
	 	
	 	# Add to docs dictionary mapping docID to file
	 	docs[docID] = fileid
	 	docID += 1
	size =  0
	for k in idx.iterkeys():
		size += os.sys.getsizeof(k)
		size += os.sys.getsizeof(idx[k])
	#print "size of original dictionary is:", size
	return idx

def dictionary_string_reuters():
	"""
	A function that creates a dictonary as a string for the 
	reuters corpus.
	"""
	original_idx = create_dictionary_index_reuters()
	sorted_list = sorted(original_idx.iterkeys())
	new_idx = {}
	term_start = 0
	dictionarystring = ""

	for key in sorted_list:
		dictionarystring += str(key)
		new_idx[term_start] = original_idx[key]
		term_start += len(key)

	size =  0
	for key in new_idx.iterkeys():
		size += os.sys.getsizeof(key)
		size += os.sys.getsizeof(new_idx[key])

	#print "size of new_idx dictionary is:", size
	return new_idx

def dictionary_string_reuters_with_blocks(blocksize):
	"""
	A function that creates a dictonary as a string with a given 
	block size for the reuters corpus.
	"""
	original_idx = create_dictionary_index_reuters()
	sorted_list = sorted(original_idx.iterkeys())
	new_idx = {}
	term_start = 0
	dictionarystring = ""

	for i in range(0, len(sorted_list), blocksize):
		block_terms_length = 0
		block_postings = []
		nextblock = i+blocksize
		# Check to see if in last block to account for 
		# remainder terms
		lastblock = blocksize * (len(sorted_list)/blocksize)
		if i == lastblock:
			nextblock = len(sorted_list)

		for j in range(i, nextblock, 1):
			key = sorted_list[j]
			block_postings.append(original_idx[key])
			length_and_key = str(len(key)) + key
			dictionarystring += length_and_key
			block_terms_length += len(length_and_key)
		
		new_idx[term_start] = block_postings
		term_start += block_terms_length


	size =  0
	for key in new_idx.iterkeys():
		size += os.sys.getsizeof(key)
		size += os.sys.getsizeof(new_idx[key])
		for postingslist in new_idx[key]:
			size += os.sys.getsizeof(postingslist)

	#print "size of new_idx dictionary with blocksize", blocksize, "is:", size
	return new_idx


if __name__ == '__main__':
    import doctest
    doctest.testmod()