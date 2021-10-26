from re import *
import sys
import os
import subprocess
import argparse

TIME_LIMIT = 180 # Second to wait for a solution

def SCIP(values_path):
	'''
		Runs SCIP solver on the model and returns whether a solution was found or not.		
	'''	
	command = 'scip.exe -c \" set limits time {} read model.zpl optimize write solution sol.out quit\"'.format(TIME_LIMIT)
	os.system(command)

	# checks whether there is some solution

	OBJECTIVE = 'objective value'
	with open('sol.out', 'r') as f:
		sol_file = f.read()
	ans = OBJECTIVE in sol_file

	return ans

def codify_text(path, text):
	'''
		Writes to path the vector form of the words passed in the string text
	'''
	occur = [0 for i in range(26)]
	for c in text:
		cod = ord(c) - ord('a')
		occur[cod] += 1

	with open(path,"w") as f:		
		for l in range(26):
			f.write(str(l+1) + " " + str(occur[l]) + "\n")

def process_string(s):
	'''
		Cleans string s from non alphabetic characters and casts to lower case.
	'''
	regenter = compile('(\n)\\1+')
	regspace = compile('( )\\1+')
	regex = compile('[^a-zA-Z .]')
	s = regex.sub('', regspace.sub(' ',regenter.sub(' ', s)) ).lower().split('.')
	s = "".join(s)

	return s

def solve_excerpt(excerpt_path, title_path, values_path):
	'''
		Tries to find a cryptogram for a given excerpt and title. It need a path to a file
		with the excerpt, another with the title and finally the path to where the values of the
		words are stored.
	'''
	with open(title_path, 'r') as f:
		title = f.read()

	with open(excerpt_path, 'r') as f:
		excerpt = f.read()
	
	excerpt = process_string(excerpt).replace(' ','')
	title = process_string(title).replace(' ','')

	codify_text('title_vector.txt', title)
	codify_text('excerpt_vector.txt', excerpt)
	
	# At this point, the optimization program is ready. If you don't have SCIP, you can run
	# > zimpl -t mps model.zpl
	# This will generate the machine readable files that can be fed to another solvers such as
	# PuLP (https://coin-or.github.io/pulp/index.html).

	ans = SCIP(values_path)	

	if ans:
		words = []
		with open('../data/values.txt', 'r') as f:
			words = f.readlines()

		cryptogram = set()
		with open('sol.out','r') as f:
			# ignore first two lines
			next(f)
			next(f)
			for line in f:
				l = line.split() # l = [name of variable, value of variable, impact on objective]
				variable = l[0]

				if variable[0] == 'x':
					# it indicates a word
					var_info = variable.split('#') # var_info = [x, identifier of word]
					index = int(var_info[1])
					w = words[index-1].split()[1]

					cryptogram.add(w)

		letter_dic = {}
		letter_ind = {}
		for i in range(len(excerpt)):
			c = excerpt[i]
			if c in letter_dic.keys():
				letter_dic[c].append(i)
			else:
				letter_dic[c] = [i]
				letter_ind[c] = 0

		# Write obtained words to cryptogram.txt in a correct order
		with open('cryptogram.txt', 'w') as f:
			for letter in title.replace(' ',''):				
				cur = ""
				for w in cryptogram:
					if(w[0] == letter):
						cur = w
						break
				cryptogram.remove(w)
				print(cur)
				indices = []
				for c in cur:
					pos = letter_ind[c]
					indices.append(letter_dic[c][pos])					
					letter_ind[c] += 1
				f.write(cur+'\n')
				f.write(str(zip(cur, indices))+'\n')

		print('Cryptogram solution written to cryptogram.txt')

	else:
		print("No solution found")

	return

def solve(book_path, title):
	'''
		Iterates through excerpts of a book in plain text and stops when a solution is found.
	'''
	codify_text('title_vector.txt', title)

	regenter = compile('(\n)\\1+')
	regspace = compile('( )\\1+')
	regex = compile('[^a-zA-Z .]')

	with open(book_path, "r") as f:
		text = f.read()
	
	# Eliminate all non-letters and cast to lowercase.
	text = regex.sub('', regspace.sub(' ',regenter.sub(' ', text)) ).lower().split('.')

	# We will consider fragments of length between lo and hi.
	l, r, totlen = 0, 0, 0
	L = len(title)
	lo, hi = 7 * L, 11 * L
	right = True
	i = 0

	while (l <= r) and r < len(text):		
		# Every analyzed excerpt consists of all the phrases comprised between indices l (inclusive) and r(exclusive).
		if right:
			line = text[r]
			for c in line:
				cod = ord(c) - ord('a')
				if(0 <= cod and cod < 26):
					totlen += 1

			r += 1
			if totlen > hi:
				right = False
			else:				
				if totlen >= lo:
					t = "".join(text[l:r])
					print(t)
					codify_text('excerpt_vector.txt', t.replace(' ',''))
					ans = SCIP()

					if ans:
						return					
		else:
			line = text[l]
			for c in line:
				cod = ord(c) - ord('a')
				if(0 <= cod and cod < 26):
					totlen -= 1
			l += 1
			if totlen < lo:
				right = True
			else:
				if totlen <= hi:
					t = "".join(text[l:r])
					print(t)
					codify_text('excerpt_vector.txt', t.replace(' ',''))
					ans = SCIP()

					if ans:
						return

	print ('Bad luck :(')
	return

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Solves the problem of finding a cryptogram given a specific excerpt and a title. The length of the excerpt should be roughly between 6 and 11 times the length of the title.')

	parser.add_argument('excerpt_path', help='The path to the file where the excerpt is written')
	parser.add_argument('title_path', help='The path to the file where the title is written')
	parser.add_argument('values_path', nargs='?', default='../data/values.txt', help='The path to the file where the values of the words are stored. If not provided, it defaults to ../data/values.txt')

	args = parser.parse_args() # parse sys.argv
	
	excerpt_path, title_path, values_path = args.excerpt_path, args.title_path, args.values_path
	solve_excerpt(excerpt_path, title_path, values_path)