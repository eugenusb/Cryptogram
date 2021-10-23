import sys

def generate_values(words_freq_path, values_path):
	'''
		Generates the value of each word as the reciprocal of its relative frequency
	'''
	with open(words_freq_path, "r") as f, open(values_path, "w") as g:
		ind = 1
		for line in f:
			l = line.split() # l = [ranking, word, count, percentage, cumulative percent]
			word = l[1]
			value = l[3][:-1]

			if len(word) >= 4:
				value = 1 / float(value)
				g.write(str(ind) + " " + word + " " + str(value) + "\n")
				ind += 1

if __name__ == '__main__':
	words_freq_path, values_path = sys.argv[1], sys.argv[2]
	generate_values(words_freq_path, values_path)