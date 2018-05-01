import hashlib

password = open('rockyou.txt').read().splitlines()
h2 = hashlib.md5("GET:/private/").hexdigest()
for i in range(len(password)):
    h1 = hashlib.md5("admin:Private Area:" + password[i]).hexdigest()
    result = hashlib.md5(h1 + ":dUASPttqBQA=7f98746b6b66730448ee30eb2cd54d36d5b9ec0c:00000001:edba216c81ec879e:auth:" + h2).hexdigest()
    if result == "3823c96259b479bfa6737761e0f5f1ee":
        print "[*] Password found: " + password[i]
        exit()
