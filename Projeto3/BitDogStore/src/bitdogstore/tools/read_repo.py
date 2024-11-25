import os
import json

# Busca por aplicativos nos repositórios
def get_apps_configs(repos: list):
    apps_configs = []
    for dir in repos:
        # Se não tiver um repo.json não é considerado um repositório
        # Portanto, é ignorado
        if not "repo.json" in os.listdir(dir):
            print("repo.json não encontrado")
            continue
        
        # Lê as informções do repo.json
        with open(f'{dir}/repo.json') as file:
            repo = json.load(file)

        # Se n tiver repository_name ou app_folder dará erro
        assert "repository_name" in repo.keys(),"repo.json sem repository_name"
        assert "apps_folder" in repo.keys(),"repo.json sem apps_folder"
        
        # Para cada app folder listed in apps_folder
        for apps_folder in repo['apps_folder']:
            apps_dir = os.path.join(dir,linux_to_os(apps_folder))
            assert os.path.exists(apps_dir),"diretorio de apps não encontrado"
            apps = os.listdir(apps_dir)
            # Para cada app será carregado suas informações de forma 
            # que seja facil para o sistema manusear
            for app in apps:
                path = os.path.join(apps_dir,app)
                if os.path.exists(os.path.join(path,'app.json')):
                    with open(os.path.join(path,'app.json')) as file:
                        config = json.load(file)
                        if config.get('micropython_config'):
                            if not config['micropython_config'].get('firmware'):
                                if repo.get('repo_micropython_firmware'):
                                    config['micropython_config']['firmware'] = os.path.join(dir,linux_to_os(repo['repo_micropython_firmware']))
                                else:
                                    file_path = os.path.realpath(__file__)
                                    file_path = file_path.removesuffix('read_repo.py')
                                    config['micropython_config']['firmware'] = os.path.join(
                                        file_path,'default.uf2')
                            else:
                                config['micropython_config']['firmware'] = os.path.join(path,linux_to_os(config['micropython_config']['firmware']))
                            for i,file in enumerate(config['micropython_config']['files']):
                                config['micropython_config']['files'][i] =  os.path.join(path,linux_to_os(file))
                        else:
                            config['c_config']['firmware'] = os.path.join(path,config['c_config']['firmware'])
                        if config.get('docs'):
                            config['docs'] = os.path.join(path,config['docs'])
                        if config.get('icon'):
                            config['icon'] = os.path.join(path,config['icon'])
                        else:
                            config['icon'] = 'empty.jpg'
                        config['path'] = path
                        apps_configs.append(config)
                config = None
            apps = None
    return apps_configs

def linux_to_os(path):
    return os.path.join(*path.split('/'))
