# from Crypto.Cipher import PKCS_v1_5 as cipher
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA

file = open('pub.key', 'r') 
text = RSA.importKey(file.read())  

p = 1332830227949273521465367319234277279439624789
q = 1371293089587387292180481293784036793076837889
e = text.e

phi = (p -1) * (q -1)

n = p*q
phi = (p-1)*(q-1)

# Took from SO
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

d = modinv(e, phi)

print('P =', p)
print('Q =', q)
print('N =', n)
print('Phi =', phi)
print('E =', e)
print('D =', d)
print('(E*D)%Phi =', (e*d)%phi) 

private_key = RSA.construct(( n, e, d, p, q ))

print(private_key.export_key('PEM').decode('ASCII'))

pk = open('pk.key','wb')
pk.write(private_key.export_key('PEM'))
pk.close()

# openssl rsautl -decrypt -in key.cipher -out key.txt -inkey pk.key
# openssl aes-256-cbc -salt -a -d -in ciphertext.enc -out aes256.txt
# openssl aes-256-cbc -md md5 -a -d -in ciphertext.enc -out message.txt

