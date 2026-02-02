const API_BASE_URL = "http://uce-reporting-alb-875399243.us-east-1.elb.amazonaws.com";

async function cargarReporteCombinado() {
  const res = await fetch(`${API_BASE_URL}/reportes/combinado`);
  const data = await res.json();

  const tbody = document.querySelector("#tablaCombinada tbody");
  tbody.innerHTML = "";

  data.forEach(q => {
    tbody.innerHTML += `
      <tr>
        <td>${q.origen}</td>
        <td>${q.nombre}</td>
        <td>${q.correo}</td>
        <td>${q.titulo}<br>${q.descripcion}</td>
        <td>${q.estado}</td>
      </tr>`;
  });
}

document.addEventListener("DOMContentLoaded", cargarReporteCombinado);
