const API_BASE_URL = "http://uce-reporting-alb-875399243.us-east-1.elb.amazonaws.com";

document.getElementById("registroForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value.trim();
  const correo = document.getElementById("correoRegistro").value.trim();
  const contraseña = document.getElementById("contraseñaRegistro").value.trim();
  const mensaje = document.getElementById("mensaje");

  if (!nombre || !correo || !contraseña) {
    mensaje.innerText = "Completa todos los campos";
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/usuarios/registro`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nombre: nombre,
        correo: correo,
        pssw: contraseña,   // 🔥 CLAVE
        rol: "cliente"
      })
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Backend error:", errorText);
      mensaje.innerText = "Error al registrar usuario";
      return;
    }

    alert("Registro exitoso");
    window.location.href = "/index.html";

  } catch (error) {
    console.error(error);
    mensaje.innerText = "Error de conexión";
  }
});
