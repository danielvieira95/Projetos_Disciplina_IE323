import hashlib

# Dado um arquivo, devolve o sha1 de seu conteúdo
def gen_hash(file):
    hasher = hashlib.new("sha1")
    with open(file, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()