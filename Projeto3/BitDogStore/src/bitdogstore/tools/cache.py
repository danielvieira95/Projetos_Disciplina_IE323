import appdirs
import os
import json
import zipfile

# Diretório da BitDogStore
user_data_dir = appdirs.user_data_dir("BitDogStore")
# Diretório da pasta repositories dentro da BitDogStore
repositories = os.path.join(user_data_dir,'repositories')

# Cria as pastas BitDogStore e repositories se não existirem 
def create_cache_dirs_if_not_exists():
    os.makedirs(user_data_dir, exist_ok=True)
    os.makedirs(repositories, exist_ok=True)
    
# Extrai o arquivo default.zip para a pasta de cache 
def extract_default_to_cache():
    if not ls_repos():
        file_path = os.path.realpath(__file__)
        file_path = file_path.removesuffix('cache.py')
        with zipfile.ZipFile(os.path.join(file_path,'default.zip'), 'r') as zip_ref:
            zip_ref.extractall(repositories)
        
# Lista todos os repositórios disponíveis
def ls_repos():
    return [os.path.join(repositories, filename) for filename in os.listdir(repositories)]

# Retorna o loca da pasta repositories
def get_repos_dir():
    return repositories
    
def get_dir():
    return repositories