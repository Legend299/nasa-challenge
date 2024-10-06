document.getElementById('fecha').valueAsDate = new Date()

document.getElementById('fechaForm').addEventListener('submit', async function (e) {
  e.preventDefault()
  const fecha = document.getElementById('fecha').value
  const response = await fetch('http://localhost:5000/predecir?fecha=' + fecha)
  const datos = await response.json()

  if (datos.error) {
    alert(datos.error)
    return
  }

  document.getElementById('resultadoIA').textContent = `${datos.prediccion_IA.toFixed(2)}%`
  document.getElementById('resultadoTX').textContent = `${datos.prediccion_TX.toFixed(2)}%`
  document.getElementById('resultadoMO').textContent = `${datos.prediccion_MO.toFixed(2)}%`
})
