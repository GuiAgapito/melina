import json
import os

CONFIG_FILE = "config.json"

def get_default_download_path():  
  return os.path.join(os.path.expanduser("~"), "Downloads")

def get_default_theme():
  return "dark"

def load_config():  
  if not os.path.exists(CONFIG_FILE):
    return {"theme": get_default_theme(), "download_path": get_default_download_path()}
  
  try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
      config = json.load(file)
      if not isinstance(config, dict):
        raise ValueError("Arquivo de configuração inválido")
            
      if "download_path" not in config:
        config["download_path"] = get_default_download_path()
      if "theme" not in config:
        config["theme"] = get_default_theme()

      return config
  except (json.JSONDecodeError, ValueError):
    return {"theme": get_default_theme(), "download_path": get_default_download_path()}

def save_config(config):  
  with open(CONFIG_FILE, "w", encoding="utf-8") as file:
    json.dump(config, file, indent=2)

def set_config(key, value):  
  config = load_config()
  if config is None: 
    config = {}
  config[key] = value
  save_config(config)
