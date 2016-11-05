import os

HAM_TRAIN_DIR = 'data/train/ham/'
SPAM_TRAIN_DIR = 'data/train/spam/'

# This function reads in a file and returns a 
# set of all the tokens. It ignores the subject line
def token_set(filename):
	#open the file handle
	with open(filename, 'r') as f:
		#ignore the Subject beginning
		text = f.read()[9:]
		#put it all on one line
		text = text.replace('\r', '')
		text = text.replace('\n', ' ')
		#split by spaces
		tokens = text.split(' ')
		#return the set of unique tokens
		return set(tokens)

def p_ham_spam():
  ham = len(os.listdir(HAM_TRAIN_DIR)) * 1.0
  spam = len(os.listdir(SPAM_TRAIN_DIR)) * 1.0
  return ham / (ham + spam), spam / (ham + spam)

p_ham, p_spam = p_ham_spam()

print 'Pr(Ham) = ' + str(p_ham)
print 'Pr(Spam) = ' + str(p_spam)
print 'Pr(Ham) + Pr(Spam) = ' + str(p_ham + p_spam)
