// Exibir notifiação
const showNotification = (type, message) => {
  let ct_notification = document.querySelector('.notifications');
  if (!ct_notification) {
    ct_notification = document.createElement('div');
    ct_notification.classList.add('notifications');
    document.body.appendChild(ct_notification);
  }

  const className = `${type}`;

  const iconMap = {
    error: 'fas fa-times-circle',
    info: 'fas fa-info-circle',
    success: 'fas fa-check-circle',
    warning: 'fas fa-exclamation-triangle'
  };

  const iconClass = iconMap[type] || '';

  const alert = document.createElement('div');
  alert.classList = `notification ${className}`;
  alert.innerHTML = `    
    <i class="${iconClass}"></i>
    <span>${message}</span>
  `;

  alert.classList.add('slide-in-initial');
  ct_notification.appendChild(alert);

  setTimeout(() => {
    alert.classList.remove('slide-in-initial');
    alert.classList.add('slide-in');
  }, 10);

  setTimeout(() => {
    alert.classList.remove('slide-in');
    alert.classList.add('slide-out');
  }, 4500);

  setTimeout(() => {
    alert.remove();
    if (!ct_notification.hasChildNodes()) {
      ct_notification.remove();
    }
  }, 3000);
};

// Playlist
let playlist = [];

// Adicionar link ao pressionar enter
document.getElementById("input-link").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    addLinkToPlaylist("input-link");
  }
})

// Adicionar link a playlist
const addLinkToPlaylist = () => {
  const input = document.getElementById("input-link");
  const value = input.value;

  // Verifica se o valor do input está vazio
  if (!value) {
    showNotification("warning", "O campo de link está vazio! Por favor, insira um link.");
    return;
  }

  // Verifica se é um link do youtube
  if (!value.startsWith("https://www.youtube.com/watch?v=")) {
    showNotification("error", "Por favor, insira um link do YouTube.");  
    return;
  }

  // Verificar se o link já está presente na playlist
  if (playlist.includes(value)) {
    showNotification("warning", "Link já adicionado.");
    return;
  }

  // Adicionar link a playlist
  playlist.push(value);  
  // Adicionar link a pagina
  addLinkToPage(value);
  // Limpa o campo de input 
  input.value = '';  
}

// Adicionar link a pagina
const addLinkToPage = (link) => {
  // Div que irá conter todos os links adicionados
  const links_list = document.getElementById("added-links");

  // Div que irá conter cada link
  const link_line = document.createElement("div");
  link_line.id = link;
  link_line.classList.add('link-line');

  // Div que irá conter o nome do link
  const link_name = document.createElement("div");
  link_name.classList.add("link-name");

  // Div que irá conter as opções do link, como copiar, abrir e remover
  const link_options = document.createElement("div");
  link_options.classList.add("link-options");  
  
  // Adiciona o link enquanto está sendo carregado o nome do video
  link_name.innerHTML = `
    <div class="spinner-container">
      <div class="spinner"></div>
    </div>
    <div>
      <p class="loading-text">Carregando...</p>
      <small>${link}</small>
    </div>    
  `;

  // Busca o nome do video e exibe na div que contém o link
  window.pywebview.api.getVideoName(link).then(response => {    
    link_name.innerHTML = `      
      <div>
        <p>${response}</p>
        <small>${link}</small>
      </div>      
    `;
  });
  
  // Adicione os botões de ações do link
  link_options.innerHTML = `  
    <a class="btn btn-primary" href="${link}" target="_blank" title="Abrir ${link}">
      <i class="fa-solid fa-link"></i>
    </a>
    <button class="btn btn-danger" onclick="removeLink('${link}')" title="Remover ${link}">
      <i class="fa-solid fa-trash"></i>
    </button>
  `;
  
  // Adiciona o link a pagina
  link_line.appendChild(link_name);
  link_line.appendChild(link_options);
  links_list.appendChild(link_line);
}

// Remover link
const removeLink = (link) => {
  // Remove o link da playlist
  playlist = playlist.filter(i => i !== link);

  // Remove o link da pagina
  document.getElementById(link).remove();
};

// Limpar playlist
const clearPlaylist = () => {
  // Limpa a playlist
  playlist.length = 0;

  // Limpa os links na página
  const links_list = document.getElementById("added-links");
  list_links.innerHTML = '';

  notification("info", "Playlist limpa com sucesso!");
}

// Selecionar caminho de download
const setDownloadPath = () => {
  const input = document.getElementById("select-download-path");
  window.pywebview.api.selectDirectory().then(function(directory) {
    input.value = directory;
  }).catch(function(error) {
    showNotification("error", `Erro: ${error}`);
  });
}

// Selecionar tema
const setTheme = (input) => {
  const theme_selected = input.value;      
  changeTheme(theme_selected);
  window.pywebview.api.setConfig("theme", theme_selected)  
  .catch(function(error) {
    showNotification("error", `Erro: ${error}`);    
  });    
}

// Buscar configs como o tema e o local de download das mídias
const getConfigs = () => {
  const inputDownloadTheme = document.getElementById("select-download-path");  
  changeTheme("dark");
  window.pywebview.api.getConfig().then(function(config){
    theme = config.theme;
    download_path = config.download_path;    

    inputDownloadTheme.value = download_path;
    const inputTheme = document.getElementById(`theme-${theme}`);
    inputTheme.checked = true; 
    changeTheme(theme);
  }).catch(function(error) {
    showNotification("error", `Erro: ${error}`);    
  })          
}

// Alterar o tema
const changeTheme = (theme) => {
  let arquive_theme = theme === "light" ? "light-mode.css" : "dark-mode.css";
  const existing_link = document.querySelector("link[href*='dark-mode.css'], link[href*='light-mode.css']");
  if (existing_link) {
    existing_link.remove();
  }

  const link_theme = document.createElement("link");
  link_theme.rel = "stylesheet";
  link_theme.href = `./../css/${arquive_theme}`;
  document.head.appendChild(link_theme);   
}

window.onload = function() {
  setTimeout(() => {
    getConfigs();
  }, 100); 
};

const toggleModal = (modalId) => {
  const modal = document.getElementById(modalId);
  modal.classList.toggle("show-modal");    
}
