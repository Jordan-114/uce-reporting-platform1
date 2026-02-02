const API_BASE_URL = "http://uce-reporting-alb-875399243.us-east-1.elb.amazonaws.com";

async function enviarQueja() {
  const titulo = document.getElementById("tituloQueja").value.trim();
  const descripcion = document.getElementById("descripcionQueja").value.trim();
  const token = localStorage.getItem("access_token");

  if (!token) {
    alert("Debes iniciar sesión");
    window.location.href = "/index.html";
    return;
  }

  const res = await fetch(`${API_BASE_URL}/quejas-web/quejas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ titulo, descripcion })
  });

  if (!res.ok) {
    alert("Error al enviar la queja");
    return;
  }

  alert("Queja enviada");
  document.getElementById("quejaForm").reset();
  cargarQuejas();
}

async function cargarQuejas() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const res = await fetch(`${API_BASE_URL}/reportes/web`, {
    headers: { "Authorization": `Bearer ${token}` }
  });

  const data = await res.json();
  const cont = document.getElementById("estadoQuejas");
  cont.innerHTML = "";

  data.forEach(q => {
    cont.innerHTML += `
      <div class="card mb-2">
        <div class="card-body">
          <b>${q.titulo}</b><br>${q.descripcion}
          <span class="badge bg-warning">${q.estado}</span>
        </div>
      </div>`;
  });
}

document.getElementById("quejaForm").addEventListener("submit", e => {
  e.preventDefault();
  enviarQueja();
});

document.getElementById("btnLogout").onclick = () => {
  localStorage.clear();
  window.location.href = "/index.html";
};

window.onload = cargarQuejas;
