import bcrypt
import time
import base64
from nltk.corpus import words
import multiprocessing
from functools import partial

#This the multiprocessed version of the bcrypt code.
#On my home computer this code takes about 3.5 hours to complete
 
def bcrypt_checker(word_list, hash_value, user):
  #checks the password attempt and returns true if it matches false otherwise
  if bcrypt.checkpw(word_list.encode('utf-8'), hash_value.encode('utf-8')):
      return ("{} is the password for {}!!".format(word_list, user))
      
  return False


if __name__ == '__main__':

  #read in words from nltk
	word_list = words.words()
  #select words that meet parameters (length is between 6 and 10)
	word_list = [w for w in word_list if 6 <= len(w) <= 10]
  
  #read in the shawdow file
	shadow = [line.rstrip() for line in open('shadow.txt', 'r')]
	#parse the information from the user
  shadow = [string.split(':') for string in shadow]
	
  #create dic of users and their hashes
  users = {}
	for i in range(len(shadow)):
		users[shadow[i][0]] = shadow[i][1]

  #for each user create a pool of processes and assign a password to each
  #process.  Once password is found terminate the pool and start again 
  #for the next password
	for usr, hash_v in users.items():
    #generate the pool
		pool = multiprocessing.Pool()
		start = time.time()
		
    #freeze the two inputs to the checker
    # ***may not be needed***
    list_checker = partial(bcrypt_checker, hash_value=hash_v, user=usr)
    #map each password to a process in the pool
		res_list = pool.imap_unordered(list_checker, word_list)
		pool.close()

    #until password is found keep trying processes
		for res in res_list:
			if res != False:
				end = time.time()
				print(res)
				print("Took {} seconds to crack!!".format(end-start))
				pool.terminate()
				break
		pool.join()
