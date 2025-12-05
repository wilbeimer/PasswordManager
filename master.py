import bcrypt

password = b"master_password_here"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed.decode())
