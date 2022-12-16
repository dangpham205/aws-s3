import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

def token_reponse(token:str):
    return {
        'access_token':token
    }

def signJWT(user_id:str)->Dict[str,str]:
    payload = {
        'user_id': user_id,
        'expires': time.time()+600
    }
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_reponse(token)

def decodeJWT(token:str, with_secret_key = True)->dict:
    try:
        if with_secret_key:
            decode_token = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        else:
            decode_token = jwt.decode(token, options={"verify_signature": False})
        # decode_token = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        return decode_token #if decode_token['expires']>= time.time() else None
    except:
        return False

if __name__ == '__main__':
    token = signJWT('user1')
    print(token)