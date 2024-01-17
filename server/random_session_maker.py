import string
import random
def random_string(length):
    characaters= string.ascii_letters + string.digits 
    random_string= ''.join(random.choice(characaters) for i in range(length))
    return random_string
