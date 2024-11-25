import os
import string
import shutil
import subprocess
import sys
import json

# Lista o conteúdo do disco
def list_directory_contents(drive):
    contents = os.listdir(drive)
    return contents

# Se o dispositivo for windows, é criada as funções abaixo
if os.name == 'nt':

    # Lista os discos monstados
    def list_mount_points():
        drives = [f"{letter}:\\" for letter in string.ascii_uppercase if os.path.exists(f"{letter}:\\")]
        return drives

    # Verifica se os arquivos INFO_UF2.TXT e INDEX.HTM estão no disco
    # caso estejam quer dizer que é uma rapsberry pi pico
    def get_mounts():
        mount_points = list_mount_points()
        correct = []
        for mount in mount_points:
            contents = list_directory_contents(mount)
            for item in contents:
                if 'INFO_UF2.TXT' and 'INDEX.HTM' in item:
                    correct.append(mount)
        return correct

    # Copia o arquivo para o disco
    def push(file, mount):
        shutil.copy(file,mount)

# Se o dispositivo for Linux, é criada as funções abaixo
elif sys.platform.startswith('linux'):

    # Verifica se o disco montado é uma rapsberry pi pico
    def get_mounts():
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,MODEL,MOUNTPOINT', '-J'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)

            if result.returncode != 0:
                print(f"Error running lsblk: {result.stderr}")
                return []

            lsblk_output = json.loads(result.stdout)

            correct = []
            for device in lsblk_output.get('blockdevices', []):
                if device['model'] == 'RP2':
                    for child in device.get('children', []):
                        mountpoint = child.get('mountpoint')
                        if mountpoint:
                            contents = list_directory_contents(mountpoint)
                            for item in contents:
                                if 'INFO_UF2.TXT' and 'INDEX.HTM' in item:
                                    correct.append(mountpoint)
                        else:
                            print(f"No mount point found for {child['name']}")
            return correct
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    # Copia o arquivo para o disco
    def push(file, mount):
        shutil.copy(file,mount)

# Se o dispositivo não for nem Linux nem Windows, dará erro
else:
    raise(Exception("OS não suportado"))
