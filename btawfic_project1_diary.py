# COMP90042 - Web Text and Search Analysis Project 1 Diary
# Bilal Tawfic (btawfic) 329904

"""
Hour 1.
Began by researching the three topics given for the project. Spent time looking
at the different IBM models as I found implementing IBM Model 1 for the 
worksheet really interesting. However, after reading about index contstruction
and after briefly looking at compression techniques for inverted indexes 
became really interested in doing this topic for the project.

Hour 2.
Read section 1 of the supplied reading (http://nlp.stanford.edu/IR-book/) and
covered the basic structure of an inverted index. Learnt that the basic
building blocks to build an inverted index are as follows:
	1. Collect documents to be indexed
	2. Tokenise the text in the documents
	3. Do linguistic preprocessing 
		- this includes making terms all lower case and stemming
	4. Index the documents that each term occurs in

Hour 3.
Read sections 4.1, 4.2 and 4.3 of the supplied reading. Learned that there are
two algorithms for index constuction. These are the block sort-based indexing 
(BSBI) algorithm and the single-pass in-memory indexing (SPIMI) algorithm. 
Decided that when I was going to implement one of these algorithms that I would
implement SPIMI because it allows for compression techniques to be used. 
Decided not read section 4.4 because distributed indexing would not be used
for this project. Also, did not read section 4.5 on dynamic indexing since it
was assumed that the dataset that would be used for the implementation would
not change at all.

Hour 4.
Read sections 5.1 and 5.2 of the supplied reading on some statistics on 
compression and about dictionary compression. Learnt that compressing a 
dictionary meant that more or all of it could be stored in the faster main
memory as opposed to on disk. This leads to higher query throughput.

Hour 5.
Read section 5.3 of the supplied reading on postings file compression. Learnt
that frequent terms occur next to each other and therefore a good idea is to 
compress the gaps between document ids in the postings list. Also, learned
that variable byte encoding is a good method becasue it offers a nice 
tradeoff between compression and time. Learnt that the more difficult bit-
manipulation algorithms are usually more complex but do offer better compression.

Hour 6.
Made a plan on how to implement this project. The plan is as follows:
	1. Collect documents to be indexed
		try to find reuters-rcv1 to match paper
	2. Tokenize the text
		since only english documents are used (for now) - use the porter stemmer
	3. Do linguistic preprocessing
		make all terms lower case
		stem all terms
		remove numbers and punctuation
	4. Index the documents that each term occurs in by creating an inverted 
	index cosisting of a dictionary and postings
	5. Use SPIMI to build an inveted index
	7. compress dictionary further by using blocked storage and front coding
	8. compress postings files using variable byte encoding		
	9. if time, try to learn gamma encoding better and implement this

Hour 7.
Created a very basic inverted index with a mapping of the terms from nltk 
reuters corpus. Did some basic preprocessing on the terms and took note that
the size of this dictionary is 9.62MB for later comparisons.

Hour 8.
Further researched SPIMI by watching a lecture online on creating an inverted
index using the algorithm. This made the algorithm a little bit clearer to me

Hour 9.
Beagn to implement SPIMI. Did some research online on how to check memory usage using Python. Found that checking memory usage in python is not easily done and because the data set was reletively small, memory would not become full at any point in time. Therefore decided to implement the algorithm just using a hard-coded variable to decide when a new block was to be created.

Hour 10.
Wrote a function that takes the documents from the nltk reuters corpus and 
creates tuples of terms and docIDs to pass to SPIMI. Found some bugs in my
initial implementation of SPIMI and fixed these.

Hour 11.
Began to implement the merging functionality for the SPIMI algorithm. Struggling to understand how this is done. Need to research this further.

Hour 12.
Spent time trying to find a reference implementation of the SPIMI algorithm 
online but with no luck. Therefore started to think of a new way to try and
implement the merging of the blocks.

Hour 13.
Discussed the problem with Steven Bird in the tutorial who recommended that
I think about how the information is stored and look at bytes using a variable
byte technique. 

Hour 14.
Began to research how variable byte encoding would be done in Python and 
looked into the functions seek(), read() and write() for file pointers as this was the recommended way to be comparing each part of the blocks written
out to disk.

Hour 15.
Researched how to get binary representations in Python. Found out that the
function bin() returns the binary representation of an integer. Therefore,
I decided to implement a dictionary mapping between terms and their given 
term ids. This is because a term id could be represented in a binary 
format for variable byte encoding algorithms.

Hour 16.
Began to implemented the variable byte encoding functions vb_encode_number, 
vb_encode and vb_decode as described in the reading. However, the bits
that are returned are not necessarily a byte. For example 2 will be 
represented as '10'. Also, still need to get set first bit to a '1' if this is
the last byte for the number.

Hour 17.
Did some research online and found the zfill function which will now allow
me to have 8 bits represent any number. Completed the implementation that
is described in the reading and tested the functions. Spent some time thinking
about how to store the binary information so that it can be later read out of 
a block when merging takes place.

Hour 18.
Decided to encode the term id and then have the next set of bytes represent
the length of the posting list to follow and then have an encoded version
of the postings list written out to disk. The purpose of the length is so 
that I know how many bytes to read before I reach the end of the postings 
list.

Hour 19.
Spent an hour to try and figure out how to write the merge function and I 
found that I was still struggling with this. In order to be able to learn 
more from the project, I have opted to give up on implementing spimi and 
decided to focus the remaining time on implementing dictionary compression
methods such as dictionary as a string and blocked storage.

Hour 20.
I found two lectures online that describe dictionary compression methods
in more detail so I spent this hour watching them. I am still unsure about
how some of the details will be implemented in Python but I will spend of 
the rest of the time implementing these two methods. 

Hour 21.
Began to implement dictionary as a string and instead of maintaining pointers
to where a term begins because I was unsure about this I used ints to
reference where a new term begins in the string. I realise that Python ints 
do not take a fixed amount of bytes and can take more or less depending on
the integer. I am also unsure of whether I should be using a dictionary to 
store the ints (that represent the start of a new term) to the postings list 
in a dictionary. However, this implementation requires 9.06MB compared to the
original 9.62MB which is a saving of about 5.8%.

Hour 22.
Began to implement blocked storage. I need to still figure out what data
structuture I need to be using here as I am unsure. The function so far
works for creating the string but if the number of terms is not divisible
by the blocksize, some terms are not processed so I still need to fix this.

Hour 23.
I decided to store postings as list of lists with the index, n, in the first 
list representing the postings list for the nth term in the block. I know
that this is not how the algorithm is meant to be implemented but I tried
this so that I could have it up and running. I fixed the bug that prevented
terms from being processed. I will now need to test this method on different
block sizes and see what happens. 

Hour 24.
I decided to test the block storage with blocksizes 4,8,16,32 and 64. The
list below describes the results I got:
	Blocksize 			Size (MB)
		4				9.28
		8				8.95
		16				8.79
		32 				8.72
		64 				8.68

It can be seen that with blocksize 4 we actually get less compression than
dictionary as a string. This is due to the way I decided to implement the
blocked storage function. However, it can be seen that as the block size
increases the compression also increases which is what is expected. The
tradeoff though is that queries take longer when compression is higher.
Based on my results I would probably use a blocksize of 8.
"""