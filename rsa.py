import math
import random


def generate_key_pair(key_length):
  """Génère une paire de clés RSA (publique et privée)."""
  p = 11
  q = 3
  n = p * q
  e = 3
  d = 7
  public_key = (n, e)
  private_key = (n, d)
  return public_key, private_key

def encrypt(message, public_key):
  """Chiffre un message (entier) avec une clé publique."""
  n, e = public_key
  ciphertext = pow(message, e, n)
  return ciphertext

def decrypt(ciphertext, private_key):
  """Déchiffre un message chiffré avec une clé privée."""
  n, d = private_key
  print(n)
  plaintext = pow(ciphertext, d, n)
  return plaintext

# Exemple d'utilisation
key_length = 1024  # Longueur de clé en bits
public_key, private_key = generate_key_pair(key_length)

message = 1234  # Message à chiffrer (entier)
print(message)
ciphertext = encrypt(message, public_key)
print("Message chiffré :", ciphertext)

decrypted_message = decrypt(ciphertext, private_key)
print("Message déchiffré :", decrypted_message)
