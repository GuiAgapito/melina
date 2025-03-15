import webview
from pytube import YouTube

def getVideoName(url):
    try:
        yt = YouTube(url)
        return yt.title
    except Exception as e:
        return f"Erro: {e}"

class API:
    def getVideoName(self, link: str):
        return getVideoName(link)

api = API()

webview.create_window("Melina", "index.html", js_api=api)
webview.start()
