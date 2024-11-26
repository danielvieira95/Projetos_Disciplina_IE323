from asyncio import sleep
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, BOLD
import bitdogstore.tools as tools
import time
import os
import json
from markdown2 import markdown  # To convert Markdown text to HTML
import re
import git
from pathlib import Path

from bitdogstore.tools import push_py
from bitdogstore.tools import gen_hash
from bitdogstore.tools import push_c
from bitdogstore.tools.find import is_micropython,find_porta
from bitdogstore.tools.cache import get_repos_dir,ls_repos,get_dir

class Install():
    def __init__(self, dev, config) -> None:
        self.dev = dev
        self.config = config
        self.changing_device = False

class BitDogStore(toga.App):
    def startup(self):
        """começo do código"""

        # inicializar variaveis padrões
        self.ports = {}
        tools.cache.create_cache_dirs_if_not_exists()
        tools.cache.extract_default_to_cache()
        self.apps = tools.read_repo.get_apps_configs(ls_repos())

        # criar widgets
        dropdown = toga.Selection(items=[], style=Pack(padding=10, flex=1))
        dropdown_refresh = toga.Button("Refresh", on_press=self.create_dropdown, style=Pack(padding=10))
        self.dropdown = toga.Box(children=[dropdown, dropdown_refresh], style=Pack(direction=ROW))
        self.create_dropdown()
        self.label = toga.Label("Selecione a placa desejada",style=Pack(padding=10, flex=1))
        self.home_button = toga.Button("Back", on_press=self.back_to_main, style=Pack(padding=10))
        self.install_button = toga.Button("Install", on_press=self.install, style=Pack(padding=10))
        self.installing = False
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.create_main_box()
        self.main_window.show()

    def create_dropdown(self, _=None):
        """Cria dropdown com placas em modo serial e modo bootload"""
        # Dropdown menu (Selection widget)
        self.ports = {}
        # acha placas em modo serial
        serial_ports = list(map(lambda x: x.device, tools.find.find_pico_porta()))
        for serial_port in serial_ports:
            self.ports[serial_port] = True

        # acha placas em modo bootload
        mount_ports = push_c.get_mounts()
        for mount_port in mount_ports:
            self.ports[mount_port] = False

        # adiciona as placas ao dropdown
        items = serial_ports + mount_ports
        self.dropdown.children[0].items = items
        self.dropdown.children[1].on_press = self.create_dropdown

    def create_dropdown_c(self, _=None):
        """Cria dropdown com placas em modo bootload"""
        # acha placas em modo bootload
        mount_ports = push_c.get_mounts()
        self.ports = {}
        for serial_port in mount_ports:
            self.ports[serial_port] = False

        # adiciona as placas ao dropdown
        self.dropdown.children[0].items = mount_ports
        self.dropdown.children[1].on_press = self.create_dropdown_c

    def create_dropdown_py(self, _=None):
        """Cria dropdown com placas em modo serial"""
        # acha placas em modo serial
        items = list(map(lambda x: x.device, tools.find.find_pico_porta()))
        self.ports = {}
        for serial_port in items:
            self.ports[serial_port] = True

        # adiciona as placas ao dropdown
        self.dropdown.children[0].items = items
        self.dropdown.children[1].on_press = self.create_dropdown_py

    def create_main_box(self):
        """Cria a pagina incial"""
        # criar botões e dropdown
        add_repo_button = toga.Button("Adicionar Repositório", on_press=self.on_add_press, style=Pack(padding=10))
        update_button = toga.Button("Atualizar Repositórios", on_press=self.update_repos, style=Pack(padding=10))
        clean_button = toga.Button("Limpar placa Selecionada", on_press=self.clean, style=Pack(padding=10))
        dropdown = toga.Box(children=[self.label, self.dropdown], style=Pack(direction=COLUMN))
        width = 300
        j = 0
        boxes_ = []
        boxes = []

        # cria os widgets para os apps
        for app in self.apps:
            j += 1
            # adiciona a imagem
            image = toga.Image(app['icon'])
            image_widget = toga.ImageView(image,style=Pack(width=width))

            # adiciona o botão
            button = toga.Button(
                app["app_name"],
                on_press=self.on_app_press,
                style=Pack(padding=10, flex=1, width=width)
            )
            button.config = app  # Store app config in the button
            box = toga.Box(children=[image_widget,button], style=Pack(direction=COLUMN))

            # coloca os botões em grid
            boxes.append(box)
            boxes_.append(toga.Box(children=boxes,style=Pack(direction=ROW)))
            if j == 5:
                j = 0
                boxes = []
                continue

        # adiciona os apps à pagina
        stuff = toga.Box(children=[add_repo_button]+[update_button]+[clean_button]+[dropdown]+boxes_, style=Pack(direction=COLUMN))
        return toga.ScrollContainer(content= stuff)

    async def open_folder_dialog(self, widget):
        await self.dialog(toga.InfoDialog("Adicionar um repositório manualmente",
            f"Para adicionar um localmente, insira-o em:\n{get_repos_dir()}"))
    
    async def update_repos(self,widget):
        """atualiza os repositorios"""
        updated_repo = []
        not_updated_repo = []
        for repo in ls_repos():
            try:
                origin = git.Repo(repo).remotes.origin
                origin.pull()
                print(f"{repo} Updated")
                updated_repo.append(repo)
            except:
                not_updated_repo.append(repo)

        await self.dialog(toga.InfoDialog("Repositórios Atualizados", f'Foram atualizados: {updated_repo}\nNão Foram: {not_updated_repo}'))

    def on_app_press(self, widget):
        """troca a tela do app no widget.config"""
        app_config = widget.config
        self.show_app_screen(app_config)
        
    def on_add_press(self, _):
        """troca para a tela de adicionar repositorio"""
        self.show_add_screen()

    def show_add_screen(self):
        """Cria a tela para cada app"""
        box = toga.Box(style=Pack(direction=COLUMN, alignment='center', padding=10))
        # Create a title
        box.add(toga.Label("Adicionar Repositórios", style=Pack(padding=(10, 0),font_size=24, font_weight=BOLD)))

        # Create a text input field
        text_input = toga.TextInput(placeholder="Insira a URL")

        # Create a button
        async def on_button_click(widget):
            try:
                git.Repo.clone_from(text_input.value, os.path.join(get_repos_dir(),os.path.splitext(os.path.basename(text_input.value))[0]))
            except Exception as e:
                await self.dialog(toga.ErrorDialog("Ocorreu um erro", f'Não foi possivel adicionar o repositório\n{e}'))
            else:
                await self.dialog(toga.InfoDialog("Sucesso", f'O repositório foi adicionado com sucesso'))

        button = toga.Button("Submit", on_press=on_button_click)
        open_folder_button = toga.Button("Como Adicionar Localmente?",on_press=self.open_folder_dialog,style=Pack(padding=10))

        # Add elements to the main box
        box.add(text_input)
        box.add(button)
        box.add(open_folder_button)
        box.add(self.home_button)

        # Set the content of the main window
        self.main_window.title = "Adicionar Repositórios"
        self.main_window.content = box

    def show_app_screen(self, appconfig):
        """Cria a tela para cada app"""
        box = toga.Box(style=Pack(direction=COLUMN, alignment='center', padding=10))
        self.create_dropdown()

        # adiciona botões e widgets
        self.install_button.config = appconfig
        box.add(self.dropdown)
        box.add(self.label)
        box.add(toga.Label(appconfig["app_name"], style=Pack(padding=(10, 0),font_size=24, font_weight=BOLD)))
        box.add(toga.Label("MicroPython"if appconfig.get('micropython_config') else "C", style=Pack(padding=(2, 0),font_size=8)))
        box.add(toga.Label(appconfig["description"], style=Pack(padding=(10, 0))))

        # adciona o readme do app
        if appconfig.get("docs"):
            with open(appconfig["docs"],"r") as readme:
                docs_md =  readme.read()

            docs_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
            docs_html = markdown(docs_md)
            docs_html = re.sub(
                    r'src="(?!http)(.*?)"',
                    rf'src="file://{Path(appconfig["path"]).as_posix()}/\1"',
                    docs_html
                 )
            docs_webview = toga.WebView(style=Pack(flex=1))
            docs_webview.set_content('file://', f"<html><body>{docs_html}</body></html>")
            docs_box.add(docs_webview)
            box.add(docs_box)
        if appconfig.get("maintainers"):
            maintainers = ', '.join(appconfig['maintainers'])
            box.add(toga.Label(maintainers, style=Pack(padding=(10, 0))))
        if appconfig.get("contacts"):
            contacts = ', '.join(appconfig['contacts'])
            box.add(toga.Label(contacts, style=Pack(padding=(10, 0))))
        if appconfig.get("website"):
            box.add(toga.Label(appconfig['website'], style=Pack(padding=(10, 0))))
        button_box = toga.Box(children=[self.home_button, self.install_button], style=Pack(direction=ROW))
        box.add(button_box)

        # troca para a nova tela
        self.main_window.content = box

    def app_is_python(self, config):
        if config.get('micropython_config'):
            return True
        else:
            return False

    def is_serial(self, port):
        return self.ports[port]

    async def install(self, widget):
        """instala um app"""
        try:
            # verificar se já está instalando algo
            if self.installing:
                return
            self.installing = True
            # desabilitar botão
            widget.enabled = False
            install_object = Install(self.dropdown.children[0].value, widget.config)
            # verificar se vai instalar um app python ou c
            if widget.config.get('micropython_config'):
                print('install_micropython')
                await self.install_micropython(install_object)
                if not await self.check_version(install_object.dev):
                    raise Exception("Há diferença entre o arquivo version e o conteúdo da placa. É necessário limpa-lá")
            else:
                print('install_c')
                # verificar se a placa está em bootmode ou não
                if self.is_serial(install_object.dev):
                    # modo serial
                    print('install_c serial')
                    await self.put_bootloader_update_firmware(install_object, install_object.config['c_config']['firmware'])
                else:
                    # modo bootload
                    print('install_c bootloader')
                    await self.update_firmware(install_object.config['c_config']['firmware'], install_object.dev)
    
            # limpar as variaveis de instalação
            print(f"installing {widget.config['app_name']} {time.time()}")
            print(f"done")
            await self.dialog(toga.InfoDialog("Instalação Concluída", f'A instalação foi concluída com sucesso'))
        except Exception as e:
            await self.dialog(toga.ErrorDialog("Instalação mal sucedida", f'Ocorreu um erro durante a instalação\n{e}'))
            raise(e)
        finally:
            self.create_dropdown()
            widget.enabled = True
            self.installing = False


    async def install_micropython(self, install_object):
        """instala um app em python na bitdog"""
        await self.check_change_micropython_firmware(install_object)
        push_py.clean_leds(install_object.dev)
        print(f"Installing {install_object.config['path']}")
        new_version = await self.gen_version(install_object.config)
        cur_version = await self.get_cur_version(install_object.dev)
        files_remove = await self.get_cur_app_files(install_object.dev)
        try:
            await self.remove_files(files_remove, install_object.dev)
        except:
            pass
        # faz instalação dos arquivos python
        for file in install_object.config['micropython_config']['files']:
            # remover caminho do sistema para ter o caminho que será salvo no BitDogLab
            destine_path = str(Path(file).as_posix()).removeprefix(str(Path(install_object.config['path']).as_posix())+'/').split('/')
            destine_name = '/'.join(destine_path)

            # se o arquivo faz parte do app não deve ser deletado
            if f'/{destine_name}' in files_remove:
                files_remove.pop(files_remove.index(f'/{destine_name}'))

            # verifica se o arquivo está na versão correta
            if cur_version:
                if new_version.get(destine_name) == cur_version.get(destine_name):
                    print(f'{destine_name} igual')
                    # pula a parte de dar sobreescrever
                    continue
            print(f'{destine_name} diferente')
            # Criar pastas
            if len(destine_path) > 1:
                for _, dir in enumerate(destine_path[:1]):
                    tools.push_py.mkdir(dir, install_object.dev)
            # sobe o arquivo python
            tools.push_py.push(file, destine_name, install_object.dev)
        await self.update_version(new_version, install_object.dev)

    async def put_bootloader_update_firmware(self, install_object:Install, firmware):
        install_object.changing_device = True
        self.put_bitdog_in_bootloader_window(install_object)
        # espera a placa entrar em bootloader
        print('changing device', install_object.changing_device)
        while install_object.changing_device:
            await sleep(0.01)
        
        await self.update_firmware(firmware, install_object.dev)
        
    async def put_bootloader_update_firmware_clean(self, install_object:Install, firmware):
            install_object.changing_device = True
            self.put_bitdog_in_bootloader_window(install_object, self.change_device_back_to_main)
            # espera a placa entrar em bootloader
            print('changing device', install_object.changing_device)
            while install_object.changing_device:
                await sleep(0.01)
            
            await self.update_firmware(firmware, install_object.dev)

    async def check_change_micropython_firmware(self, install_object:Install):
        """verifica se precisa subir o firmware do micropython e sobe se necessário"""
        # gera o hash do firmware querido
        new_firmware = gen_hash(install_object.config['micropython_config']['firmware'])
        print('self.ports',self.is_serial(install_object.dev), install_object.dev)
        
        # verifica se o bitdog está em modo bootload ou serial
        if self.is_serial(install_object.dev):
            # modo serial
            # verifica se está com micropython instalado
            if not is_micropython(find_porta(install_object.dev)):
                # não é micropython
                print("Mudando Firmware para micropython")
                await self.put_bootloader_update_firmware(install_object, install_object.config['micropython_config']['firmware'])

                # escolher placa serial correta
                install_object.changing_device = True
                self.choose_correct_serial_bitdog_window(install_object)
                # espera a placa entrar em bootloader
                while install_object.changing_device:
                    await sleep(0.01)
                await self.remove_files(push_py.ls(install_object.dev),install_object.dev)
            else:
                # é micropython
                try:
                    # procura o arquivo com o hash do firmware dentro do micropython
                    cur_firmware = push_py.get('firmware',install_object.dev).decode()
                except:
                    # não achou o arquivo
                    cur_firmware = None

                # verifica se os hashes são diferentes
                if new_firmware != cur_firmware:
                    # troca o firmware
                    print('Firmware Diferente')
                    await self.put_bootloader_update_firmware(install_object, install_object.config['micropython_config']['firmware'])

                    # escolher placa serial correta
                    install_object.changing_device = True
                    self.choose_correct_serial_bitdog_window(install_object)
                    # espera a placa entrar em bootloader
                    while install_object.changing_device:
                        await sleep(0.01)
                    await self.remove_files(push_py.ls(install_object.dev),install_object.dev)
        else:
            # modo boot
            # troca o firmware
            await self.update_firmware(install_object.config['micropython_config']['firmware'], install_object.dev)
            self.firmware_updated = True
            self.choose_correct_serial_bitdog_window(install_object)
            while self.firmware_updated:
                await sleep(0.01)
            await self.remove_files(push_py.ls(install_object.dev),install_object.dev)
        self.create_firmware(new_firmware, install_object.dev)

    def create_firmware(self, new_firmware, dev):
        """cria arquivo de versão para o firmware e sobe na bitdog"""
        path = os.path.join(get_dir(), 'firmware')
        with open(path, 'w') as file:
            file.write(new_firmware)
        tools.push_py.push(path, 'firmware', dev)
        os.remove(path)

    async def remove_files(self, files, dev):
        """remove arquivos antigos que não fazem parte do app"""
        for file in files:
            try:
                push_py.rm(file, dev)
            except:
                push_py.rmdir(file, dev)
            print(f'arquivo {file} apagado')

    async def get_cur_version(self, dev):
        """pega a versão dos arquivos que estão no bitdog"""
        try:
            cur_version = json.loads(push_py.get('version.json', dev))
        except:
            cur_version = None

        return cur_version

    async def get_cur_app_files(self, dev):
        """pega os arquivos do bitdog que vão ser possivelmente removidos"""
        files_remove = push_py.ls(dev)
        # exclui o arquivo de versão do firmware
        if '/firmware' in files_remove:
            files_remove.remove('/firmware')
        # exclui o arquivo de versão dos arquivos do app
        if '/version.json' in files_remove:
            files_remove.remove('/version.json')
        return files_remove

    async def update_version(self, new_version, dev):
        """atualiza o arquivo de versão dos arquivos do app python"""
        path = os.path.join(get_dir(), 'version.json')
        with open(path, 'w') as file:
            json.dump(new_version,file)
        # TODO: mudar para o cache
        tools.push_py.push(path, 'version.json', dev)
        os.remove(path)

    def windows_path_to_linux(self, path:str):
        return path.replace(r'\\', '/')

    def back_to_main(self, _):
        """Return to the main screen."""
        self.main_window.content = self.create_main_box()

    def put_bitdog_in_bootloader_window(self, install_object:Install, on_press=None):
        """tela para colocar o bitdog em modo bootload"""
        if not on_press:
            on_press = self.change_device_install_object_go_back
        self.create_dropdown_c()
        box = toga.Box(style=Pack(direction=COLUMN, alignment='center', padding=10))
        label = toga.Label("Coloque a BitDogLab em mode bootload clique em refresh e escolha a placa certa", style=Pack(padding=(10, 0)))

        box.add(self.dropdown)
        box.add(self.label)
        box.add(label)
        button = toga.Button("Ok", on_press=on_press, style=Pack(padding=10))
        button.install_object = install_object
        box.add(button)

        self.main_window.content = box
        
    def change_device_back_to_main(self, widget):
        install_object:Install = widget.install_object
        dev = self.dropdown.children[0].value
        if not dev:
           return 
        install_object.dev = dev
        install_object.changing_device = False
        self.back_to_main(widget)

    def change_device_install_object_go_back(self, widget):
        install_object:Install = widget.install_object
        dev = self.dropdown.children[0].value
        if not dev:
           return 
        install_object.dev = dev
        install_object.changing_device = False
        self.show_app_screen(install_object.config)

    def choose_correct_serial_bitdog_window(self, install_object:Install, on_press=None):
        """window for selecting a device after python firmware install"""
        if not on_press:
            on_press = self.change_device_install_object_go_back
        self.create_dropdown_py()
        box = toga.Box(style=Pack(direction=COLUMN, alignment='center', padding=10))
        label = toga.Label("Selecione o BitDogLab Correto", style=Pack(padding=(10, 0)))

        box.add(self.dropdown)
        box.add(self.label)
        box.add(label)
        button = toga.Button("Ok", on_press=on_press, style=Pack(padding=10))
        button.install_object = install_object
        box.add(button)

        self.main_window.content = box

    async def gen_version(self, config):
        """gera a versão dos arquivos"""
        version = {}
        for file in config['micropython_config']['files']:
            hash = gen_hash(file)
            file = str(Path(file).as_posix())
            destine_path = file.removeprefix(str(Path(config['path']).as_posix())+'/')
            version[destine_path] = hash
        return version

    async def update_firmware(self,firmware, mount):
        """atualiza o firmware da placa"""
        # sobe o firmware novo
        push_c.push(firmware,mount)
        # espera até o firmware terminar de subir
        cur_mounts = push_c.get_mounts()
        while mount in cur_mounts:
            cur_mounts = push_c.get_mounts()
            await sleep(0.5)

    async def check_version(self, dev):
        version = json.loads(push_py.get('version.json', dev))
        print(version)
        for file in version:
            try:
                print(f'{file} is OK')
                push_py.get(file,dev)
            except Exception as e:
                print(f'{file} is missing')
                return False
        return True
        
    async def clean(self,widget):
        install_object = Install(self.dropdown.children[0].value,[])
        await self.put_bootloader_update_firmware_clean(install_object, push_py.get_default_firmware())
        install_object.changing_device = True
        self.choose_correct_serial_bitdog_window(install_object, self.change_device_back_to_main)
        while install_object.changing_device:
            await sleep(0.01)
        push_py.clean_leds(install_object.dev)
        push_py.remove_dir(install_object.dev)
        new_firmware = gen_hash(push_py.get_default_firmware())
        self.create_firmware(new_firmware, install_object.dev)
        await self.dialog(toga.InfoDialog("Limpeza Concluída", f'A Limpeza foi concluída com sucesso'))
def main():
    return BitDogStore()
