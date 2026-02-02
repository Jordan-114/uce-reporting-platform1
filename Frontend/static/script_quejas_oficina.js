const API_BASE_URL = "http://uce-reporting-alb-875399243.us-east-1.elb.amazonaws.com";

async function enviarQueja() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  const data = {
    nombre_cliente: nombre.value,
    correo_cliente: correo.value,
    titulo: tituloQueja.value,
    descripcion: descripcion.value
  };

  await fetch(`${API_BASE_URL}/quejas/oficina`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });

  alert("Queja registrada");
  formQueja.reset();
  cargarQuejasOficina();
}

async function cargarQuejasOficina() {
  const token = localStorage.getItem("access_token");
  const res = await fetch(`${API_BASE_URL}/reportes/oficina`, {
    headers: { "Authorization": `Bearer ${token}` }
  });

  const data = await res.json();
  const tbody = document.querySelector("#tablaQuejasOficina tbody");
  tbody.innerHTML = "";

  data.forEach(q => {
    tbody.innerHTML += `
      <tr>
        <td>${q.id_queja}</td>
        <td>${q.nombre_cliente}</td>
        <td>${q.correo_cliente}</td>
        <td>${q.titulo}</td>
        <td>${q.descripcion}</td>
        <td>${q.estado}</td>
      </tr>`;
  });
}

formQueja.addEventListener("submit", e => {
  e.preventDefault();
  enviarQueja();
});

window.onload = cargarQuejasOficina;
