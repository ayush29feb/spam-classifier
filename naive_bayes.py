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

def p_w(word, words_count, email_count, mem):
  if word in mem:
    return mem[word]
  ret = (1.0 + (0 if word not in words_count else words_count[word])) / (2.0 + email_count)
  mem[word] = ret
  return ret

def classify(filename, ham_words, spam_words, ham_count, spam_count, ham_p_mem, spam_p_mem):
  tokens = token_set(filename)
  prod_tokens_ham = math.log(ham_count / (ham_count + spam_count))
  prod_tokens_spam = math.log(spam_count / (ham_count + spam_count))
  for token in tokens:
    prod_tokens_ham += math.log(p_w(token, ham_words, ham_count, ham_p_mem))
    prod_tokens_spam += math.log(p_w(token, spam_words, spam_count, spam_p_mem))

  return prod_tokens_spam > (prod_tokens_ham)

def test():
  ham_count = len(os.listdir(HAM_TRAIN_DIR)) * 1.0
  spam_count = len(os.listdir(SPAM_TRAIN_DIR)) * 1.0
  ham_words = read_emails(HAM_TRAIN_DIR)
  spam_words = read_emails(SPAM_TRAIN_DIR)
  ham_p_mem = {}
  spam_p_mem = {}
 
  emails = sorted(os.listdir(TEST_DIR), key=lambda x: int(x[:len(x) - 4]))
  for email in emails:
    print email + (' spam' if classify(TEST_DIR + email, ham_words, spam_words, ham_count, spam_count, ham_p_mem, spam_p_mem) else ' ham')

def spamminess():
  ham_count = len(os.listdir(HAM_TRAIN_DIR)) * 1.0
  spam_count = len(os.listdir(SPAM_TRAIN_DIR)) * 1.0
  ham_words = read_emails(HAM_TRAIN_DIR)
  spam_words = read_emails(SPAM_TRAIN_DIR)
  ham_p_mem = {}
  spam_p_mem = {}

  all_words = []
  all_words.extend(ham_words.keys())
  all_words.extend(spam_words.keys())
  all_words = set(all_words)

  ret = None
  ret_p = 0

  for word in all_words:
    p = p_w(word, spam_words, spam_count, spam_p_mem) / p_w(word, ham_words, ham_count, ham_p_mem)
    ret = word if p > ret_p else ret
    ret_p = p if p > ret_p else ret_p

  print ret_p
  return ret

test()
print spamminess()
