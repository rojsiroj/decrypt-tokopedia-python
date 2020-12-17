# Muhamad Sirojudin <rojsiroj | sirojudin.dev@gmail.com>
import base64
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256, SHA1
from Crypto.PublicKey import RSA

def decrypt_tokopedia(secret_response, content_response):
	# Create Key
	bsecret_response = base64.b64decode(secret_response)
	rsa_key = RSA.importKey(open('your_rsa_private_file').read()) #Load Your RSA Private Key as a file
	cipher = PKCS1_OAEP.new(key=rsa_key, hashAlgo=SHA256)
	key = cipher.decrypt(bsecret_response)

	# Content
	bcontent = base64.b64decode(content_response)
	bnonce = bcontent[(len(bcontent)-12):len(bcontent)]
	bcipher = bcontent[:(len(bcontent)-12)]

	# Default Tag
	taglength = 16
	tag = bcipher[(len(bcipher)-taglength):len(bcipher)]
	acipher = bcipher[0:(len(bcipher)-taglength)]

	# Create cipher
	cipher = AES.new(key, AES.MODE_GCM, bnonce)
	decrypted = cipher.decrypt_and_verify(acipher, tag)

	# Result
	return json.loads(decrypted.decode())
