import webview
import threading
import tkinter as tk
from tkinter import filedialog
from yt_dlp import YoutubeDL
from backend.config import load_config, set_config, get_default_download_path

class API:
  def __init__(self):    
    self.config = load_config()
    if not self.config.get("download_path"):
      set_config("download_path", get_default_download_path())
  
  def getVideoName(self, url: str):    
    try:
      ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'noplaylist': True,
        'no_warnings': True,
      }
      with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", "Título não encontrado")
    except Exception as e:
      return f"Erro: {e}"

  def selectDirectory(self):    
    directory = None
    
    def _select():
      nonlocal directory
      root = tk.Tk()
      root.withdraw()
      directory = filedialog.askdirectory(title="Selecione um diretório")
      root.destroy()

    thread = threading.Thread(target=_select)
    thread.start()
    thread.join()

    if directory:
      set_config("download_path", directory)
    return directory if directory else load_config().get("download_path")

  def getConfig(self):    
    return load_config()

  def setConfig(self, key, value):    
    set_config(key, value)

api = API()
webview.create_window("Melina", "index.html", js_api=api, width=1000, height=600)
webview.start()
