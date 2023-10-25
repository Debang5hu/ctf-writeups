#!/bin/bash/env python

import bcrypt
import base64


HASH = b'$2b$12$LJ3m4rzPGmuN1U/h0IO55.3h9WhI/A0Rcbchmvk10KWRMWe4me81e'
SALT = b'$2b$12$LJ3m4rzPGmuN1U/h0IO55.'

with open('/usr/share/wordlists/rockyou.txt' , encoding = 'latin-1') as fh:
	content = fh.readlines()

	for x in content:
		try:
			passw = x.strip().encode('ascii')
			b64str = base64.b64encode(passw)
			hashAndSalt = bcrypt.hashpw(b64str,SALT)

			if hashAndSalt == HASH:
				print(f'Password Cracked: {passw} --> Hashed: {hashAndSalt}')
				break
		except:
			pass
