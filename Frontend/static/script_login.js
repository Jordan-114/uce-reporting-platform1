const API_BASE_URL = "http://uce-reporting-alb-875399243.us-east-1.elb.amazonaws.com";

document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const correo = document.getElementById("correo").value.trim();
  const pssw = document.getElementById("contraseña").value.trim();
  const mensaje = document.getElementById("mensaje");

  mensaje.innerText = "";

  if (!correo || !pssw) {
    mensaje.innerText = "Completa todos los campos";
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/usuarios/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ correo, pssw })
    });

    const data = await res.json();

    if (!res.ok) {
      mensaje.innerText = data.detail || "Error de login";
      return;
    }

    // Guardar token y rol
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("rol", data.rol);

    // Redirección por rol
    if (data.rol === "admin") {
      window.location.href = "admin.html";
    } else if (data.rol === "empleado") {
      window.location.href = "empleado.html";
    } else {
      window.location.href = "cliente.html";
    }

  } catch (error) {
    console.error(error);
    mensaje.innerText = "Error de conexión con el servidor";
  }
});
