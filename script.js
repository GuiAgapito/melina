let playlist = [];

document.getElementById("input-link").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    addLinkToPlaylist("input-link");
  }
})

const addLinkToPlaylist = (inputId) => {
  const input = document.getElementById(inputId);
  const value = input.value;

  if (!value) {
    showNotification("warning", "Por favor, adicione um link.");
    return;
  }

  // if (!value.startsWith("https://www.youtube.com/watch?v=")) {
  //   notification("error", "Por favor, insira um link do YouTube.");  
  //   return;
  // }

  if (playlist.includes(value)) {
    showNotification("warning", "Link já adicionado.");
    return;
  }

  playlist.push(value);
  getInfoVideo(value).then(console.log);;
  addLinkToPage(value);
  input.value = '';
  console.log(playlist);
}

const addLinkToPage = (link) => {
  const links_list = document.getElementById("added-links");
  const link_line = document.createElement("div");
  link_line.id = link;
  link_line.classList.add('link-line');

  const link_name = document.createElement("div");
  link_name.classList.add("link-name");

  const link_options = document.createElement("div");
  link_options.classList.add("link-options");

  window.pywebview.api.getVideoName(link).then(response => {
    link_name.innerHTML = `<a href="${link}" target="_blank">${response}</a>`;
  });

  link_options.innerHTML = `<button class="btn btn-danger" onclick="removeLink('${link}')" title="Remover ${link}"><i class="fa-solid fa-trash"></i></button>`;

  link_line.appendChild(link_name);
  link_line.appendChild(link_options);
  links_list.appendChild(link_line);
}

const removeLink = (link) => {
  playlist = playlist.filter(i => i !== link);
  document.getElementById(link).remove();
};

const clearPlaylist = () => {
  playlist.length = 0;
  notification("info", "Playlist limpa com sucesso!");
}

const showNotification = (type, message) => {
  let ctNotification = document.querySelector('.notifications');
  if (!ctNotification) {
    ctNotification = document.createElement('div');
    ctNotification.classList.add('notifications');
    document.body.appendChild(ctNotification);
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
  ctNotification.appendChild(alert);

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
    if (!ctNotification.hasChildNodes()) {
      ctNotification.remove();
    }
  }, 3000);
};

