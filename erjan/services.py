from random import randint

def generate_OTP_code():
    code = randint(100000, 999999)
    return code

def verify_OTP_code(code, user_code):
    if code == user_code:
        return True
    else:
        return False