# imports
import os
import math

# constants
HAM_TRAIN_DIR = 'data/train/ham/'
SPAM_TRAIN_DIR = 'data/train/spam/'
TEST_DIR = 'data/test/'
CUTOFF = 0.9

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

def read_emails(dirname):
  ret = {}
  emails = os.listdir(dirname)
  for email in emails:
    tokens = token_set(dirname + email)
    for token in tokens:
      ret[token] = 1 + ret[token] if token in ret else 1
  return ret

def p_w(word, words_count, email_count):
  return (1.0 + (0 if word not in words_count else words_count[word])) / (2.0 + email_count)

def classify(filename):
  ham_count = len(os.listdir(HAM_TRAIN_DIR)) * 1.0
  spam_count = len(os.listdir(SPAM_TRAIN_DIR)) * 1.0
  ham_words = read_emails(HAM_TRAIN_DIR)
  spam_words = read_emails(SPAM_TRAIN_DIR)
  
  tokens = token_set(filename)
  prod_tokens_ham = math.log(ham_count / (ham_count + spam_count))
  prod_tokens_spam = math.log(spam_count / (ham_count + spam_count))
  for token in tokens:
    prod_tokens_ham += math.log(p_w(token, ham_words, ham_count))
    prod_tokens_spam += math.log(p_w(token, spam_words, spam_count))

  return prod_tokens_spam > (math.log(9) + prod_tokens_ham)

def test():
  emails = sorted(os.listdir(TEST_DIR), key=lambda x: int(x[:len(x) - 4]))
  for email in emails:
    print email + (' spam' if classify(TEST_DIR + email) else ' ham')

test()

