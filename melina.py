import platform
import os
import yt_dlp
from colorama import Fore, Style, init

init(autoreset=True)

playlist = []

def create_download_folder():
  folder = os.path.join(os.path.expanduser("~/Downloads"), "Melina - Midias baixadas")
  os.makedirs(folder, exist_ok=True)
  return folder

def open_folder():
  path_folder = create_download_folder()
  print(f"\nPasta de downloads: {path_folder}")

  commands = {
    "Windows": f'start "" "{path_folder}"',
    "Linux": f"xdg-open '{path_folder}'",
    "Darwin": f"open '{path_folder}'"
  }

  os.system(commands.get(platform.system(), "echo 'Sistema não suportado.'"))

def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')

def add_link_to_playlist(link):
  if link not in playlist:
    playlist.append(link)
    return True
  else:    
    return False

def init_download(format_download):
  while True:
    link = input("\nDigite o link do YouTube ou tecle enter para iniciar o download: ")
    
    if link == '':
      print("\nIniciando download...")
      
      c = 0
      for link in playlist:
        c += 1
        download(link, format_download)          
        print(f"{c}/{len(playlist)}")
      playlist.clear()          
      break
    else:
      if not add_link_to_playlist(link):          
        print("\nLink duplicado, tente novamente.")

def download(link, format_type):
    folder_destination = create_download_folder()
    
    ffmpeg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ffmpeg', 'bin', 'ffmpeg.exe')
    
    ydl_opts = {
      'quiet': True,  # Oculta logs padrão
      'no_warnings': True,  # Oculta avisos
      'logger': None,  # Remove loggers do yt_dlp
      'ffmpeg_location': ffmpeg_path, # Especifica o caminho do ffmpeg.exe
    }
    
    if format_type.upper() == 'MP3':
      ydl_opts.update({
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
        }],
        'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
      })
    
    elif format_type.upper() == 'MP4':
      ydl_opts.update({
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
      })    
    
    try:
      # Redireciona saída padrão e erro para /dev/null (oculta completamente)
      with open(os.devnull, 'w') as devnull:
        original_stdout = os.sys.stdout
        original_stderr = os.sys.stderr
        os.sys.stdout = devnull
        os.sys.stderr = devnull
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([link])
      
      os.sys.stdout = original_stdout
      os.sys.stderr = original_stderr
      
      print(Fore.GREEN + f"✔ Download concluído: {link}" + Style.RESET_ALL)
      return True
    except:
      os.sys.stdout = original_stdout
      os.sys.stderr = original_stderr
      print(Fore.RED + f"✖ Ocorreu um erro ao realizar o download do link: {link}" + Style.RESET_ALL)
      return False

create_download_folder()
clear_console()

print("Bem-vindo ao Melina! Baixe suas mídias do YouTube nos formatos MP3 e MP4 de forma fácil e rápida.")

while True:
  format_download = input("\nEscolha o formato de download: \n1 - MP3 \n2 - MP4\n3 - Abrir pasta de downloads\n4 - Sair\n\n : ")
  
  if format_download == '1':
    format_download = 'MP3'    
    
    print('\nFormato escolhido: ' + format_download)        
    
    init_download(format_download)
        
  elif format_download == '2':
    format_download = 'MP4'
    print('\nFormato escolhido: ' + format_download)
    
    init_download(format_download)
            
  elif format_download == '3':
    print("\nAbrindo pasta de downloads Melina...")
    open_folder()
    
  elif format_download == '4':
    print("\nObrigado por usar o Melina! Volte sempre!")
    break
  
  else:
    print("\nOpção inválida! Tente novamente.")                 