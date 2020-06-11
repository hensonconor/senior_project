import bcrypt
import time
import base64
from nltk.corpus import words

#This code is the serial version and on my home computer
#it takes about 25 hours to finish

if __name__ == '__main__':
  
  #read in words from nltk.corpus
  word_list = words.words()
  #select works that are between 6 and 10 inclusive
  word_list = [w for w in word_list if 6 <= len(w) <= 10]
  
  #read in the shadow.txt file  
  shadow = [line.rstrip() for line in open('shadow.txt', 'r')]
  #parse each user in the shadow text file 
  shadow = [string.split(':') for string in shadow]
  
  #make a dic of users with their hash values
  users = {}
  for i in range(len(shadow)):
    users[shadow[i][0]] = shadow[i][1]
  
  #try every words for each user until a password is found
  for user, hash_value in users.items():
    start = time.time()
    for word in word_list:
      if bcrypt.checkpw(word.encode('utf-8'), hash_value.encode('utf-8')):
        end = time.time()
        #print out the passwords that was found and the time taken
        print("{} is the password for {}!!".format(word, user))
        print("Took {} seconds to crack!!".format(end-start))
        break
