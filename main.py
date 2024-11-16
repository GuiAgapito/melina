import os
import platform
import yt_dlp
import pyperclip
import flet as ft

# Coleção de links
url_collection = []

# Cria uma pasta para armazenar mídias baixadas
def create_download_folder():
    folder_path = os.path.expanduser("~/Downloads")
    folder = os.path.join(folder_path, "YDT - Midias baixadas")
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

create_download_folder()

# Realiza o download de mídia (MP3 ou MP4)
def download_media(link, format_type):        
    folder_destination = create_download_folder()
    
    ydl_opts = {}
    
    if format_type.upper() == 'MP3':
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
        }
    
    elif format_type.upper() == 'MP4':
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(folder_destination, '%(title)s.%(ext)s'),
        }    
      
    try:                     
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info = ydl.extract_info(link, download=True)        

        return True
    except Exception as e:
        return False

# Limpa todos os links da coleção de links
def clear_url_collection():
    url_collection.clear()

# Adiciona um link à coleção de links
def add_url_to_collection(url):    
    url_collection.append(url)    

# Remove um link da coleção de links
def remove_url_from_collection(i):    
    del url_collection[i]
    
def main(page: ft.Page):
    page.title = 'Melina '
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignament = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START 
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="#3A8096")
    page.update()
    
    def show_message(success, message):        
        if success:
            bg_color = '#059669'
        else:
            bg_color = '#991b1b'
    
        page.show_snack_bar(
            ft.SnackBar(
            content = ft.Text(message, color='#FFFFFF'), 
            bgcolor = bg_color  
            )
        )
        
    def add_url(e):
        if field_link.value != '' and field_link.value not in url_collection:
            group_view_links.visible = True
            link = field_link.value            
            add_url_to_collection(link)
            field_link.value = ''            
            field_link.focus()   
            update_view_links()                     
        else:
            show_message(False, 'Link duplicado ou vazio!')
    
    def remove_link(e, i):
        remove_url_from_collection(i)
        update_view_links()        
        show_message(True, f'Link removido com sucesso!')
    
    def copy_link(e, url):
        pyperclip.copy(url)    
        show_message(True, f'Link {url} copiado com sucesso!')
    
    def clear_links(e):
        group_view_links.visible = False
        url_collection.clear()
        page.update()                
        show_message(True, 'Lista de links limpa com sucesso!')
            
    def update_view_links():
        group_view_links.rows.clear()
        
        if len (url_collection) == 0:
            group_view_links.visible = False
            page.update()
            return
        
        for i, link in enumerate(url_collection):
            btn_delete = ft.IconButton(icon = ft.icons.DELETE, tooltip = 'Remover link', on_click = lambda e, index=i: remove_link(e, index))
            btn_copy = ft.IconButton(icon = ft.icons.COPY, tooltip = 'Copiar link', on_click = lambda e, link=link: copy_link(e, link))
            
            group_view_links.rows.append(
                ft.DataRow(cells = [
                    ft.DataCell(
                        ft.Text(f'{i+1} - {link}')                        
                    ),
                    ft.DataCell(
                        ft.Row([
                            btn_delete,
                            btn_copy
                        ])
                    )
                ])
            )
                        
        page.update()        
    
    def open_folder(e):
        path_folder = create_download_folder()
        print(path_folder)
        if platform.system() == "Windows":
            os.startfile(path_folder)  # No Windows, os.startfile já abre o explorador de arquivos
        elif platform.system() == "Linux":
            os.system(f"xdg-open '{path_folder}'")  # No Linux, usamos o xdg-open para abrir a pasta
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{path_folder}'")  # No macOS, o comando é 'open'
        else:
            print("Sistema operacional não suportado para abertura automática de pastas.")
    
    def init_download(e):
        if not url_collection:
            show_message(False, 'Nenhum link adicionado!')
            return
        
        if field_format_file.value is None:
            show_message(False, 'Por favor, selecione o formato que deseja realizar o download.')                
            return
        
        show_message(True, 'Iniciando download...')
        
        group_view_links.visible = False
        group_progress_bar.visible = True       
        btn_init_download.visible = False
        btn_clear_links_collection.visible = False         
        page.update()
        
        count = 0        
        
        for link in url_collection:
            download_media(link, field_format_file.value)                                           
            count += 1
            
        if count == len(url_collection):
            clear_url_collection()
            show_message(True, 'Download concluído com sucesso!')
            group_view_links.visible = False
            group_progress_bar.visible = False       
            btn_init_download.visible = True
            btn_clear_links_collection.visible = True 
        
        page.update()
                    
    group_title = ft.Column(
        controls = [
            ft.Container(
                content = ft.Text('Melina', size = 20, weight = ft.FontWeight.W_500),
                alignment = ft.alignment.center
            )
        ]
    )
    
    field_link = ft.TextField(border_color = "#EEEEEE", border_radius = 15, autofocus = True, on_submit = add_url)
    btn_add_link = ft.FloatingActionButton(text = 'Adicionar', height = 55, on_click = add_url)    
    group_field_link = ft.Column(
        controls = [
            ft.Text('Link do vídeo: ', weight = ft.FontWeight.W_700),
            ft.ResponsiveRow([
                ft.Container(
                    field_link,
                    col = {"xs": 12,"sm": 12, "md": 9, "xl": 10}
                ),
                ft.Container(
                    btn_add_link,
                    col = {"xs": 12,"sm": 12, "md": 3, "xl": 2},                    
                )
            ])
        ]
    )
    
    field_format_file = ft.RadioGroup(
        content = ft.Column([
            ft.Radio(value = 'MP3', label = 'MP3 - Apenas áudio'),
            ft.Radio(value = 'MP4', label = 'MP4 - Áudio e vídeo')
        ])
    )    
    group_field_format_link = ft.Column(
        controls = [
            ft.Text('Selecione o formato do download:', weight = ft.FontWeight.W_700),
            ft.Container(
                field_format_file                
            )
        ]
    )
    
    group_view_links = ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text('Links Adicionados', color = "#ffffff")),
            ft.DataColumn(ft.Text('Ações', color = "#ffffff"), numeric = True)
        ],
        rows = [],
        visible = False
    )
    
    btn_init_download = ft.FloatingActionButton(text = "Iniciar Download", width = 200, height = 50, on_click = init_download)
    btn_clear_links_collection = ft.FloatingActionButton(text = "Esvaziar Lista", width = 200, height = 50, on_click = clear_links)
    btn_open_folder = ft.FloatingActionButton(text = "Pasta de Downloads", width = 200, height = 50, on_click = open_folder)    
    group_btns_action = ft.Container(    
        content = ft.ResponsiveRow([
            ft.Container(
                btn_init_download,
                col = {"xs": 4,"sm": 4, "md": 4, "xl": 4},
                alignment = ft.alignment.center_right,                                     
            ),
            ft.Container(
                btn_clear_links_collection,
                col = {"xs": 4,"sm": 4, "md": 4, "xl": 4},    
                alignment = ft.alignment.center,                            
            ),
            ft.Container(
                btn_open_folder,
                col = {"xs": 4,"sm": 4, "md": 4, "xl": 4},
                alignment = ft.alignment.center_left,                
            ),
        ]),
        alignment = ft.alignment.bottom_center,
        visible = True
    )    
    
    progress_bar = ft.ProgressBar(visible = True)    
    group_progress_bar = ft.Column(
        controls = [
            ft.Container(
                content = ft.Text('Download em andamento...', size = 16, weight = ft.FontWeight.W_400),
                alignment = ft.alignment.center,                
            ),
            ft.Container(
                content = progress_bar,
                margin = ft.margin.only(bottom = 30)
            )            
        ],
        visible = False        
    )
    
    main_group = ft.Container(
        padding = ft.padding.all(20),
        width = 1000,
        content = ft.ResponsiveRow(
            columns = 12,
            spacing = 0,
            run_spacing = 30,
            controls = [
                group_title,
                group_field_link,
                group_field_format_link,
                group_view_links,
                group_progress_bar,
                group_btns_action
            ]
        )        
    )
    
    page.add(main_group)
    
ft.app(target = main)