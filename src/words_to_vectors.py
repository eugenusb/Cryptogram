import sys

def words_to_vectors(values_path, mask_path, initials_path):
	'''
		Populates two files, mask_path and initials_path with the *vector* codification of words and initials respectively.
		So, for instance the word "after", would be codified as a vector of length 26 with zeros in all positions except
		position 0 (a), position 4 (e), position 5 (f), position 12 (r) and position 14 (t). Regarding its initial, of course
		it will be represented as a vector of 26 elements with a one in position 0 (a) and zeros elsewhere.
	'''
	with open(values_path, "r") as f, open(mask_path, "w") as g, open(initials_path, "w") as h:
		for line in f:
			l = line.split() # l = [index, word, value]
			index = l[0]
			word = l[1]
			occur = [0 for i in range(26)]
			ini = [0 for i in range(26)]

			for c in word:
				cod = ord(c) - ord('a')
				occur[cod] += 1
			s = " ".join([str(o) for o in occur])
			g.write(s + "\n")

			initial = ord(word[0]) - ord('a')
			ini[initial] += 1

			t = " ".join([str(i) for i in ini])
			h.write(t + "\n")

if __name__ == '__main__':
	values_path, mask_path, initials_path = sys.argv[1], sys.argv[2], sys.argv[3]
	words_to_vectors(values_path, mask_path, initials_path)