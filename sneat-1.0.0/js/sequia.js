document.getElementById('fecha').valueAsDate = new Date()

document.getElementById('fechaForm').addEventListener('submit', async function (e) {
  e.preventDefault()

  const fecha = document.getElementById('fecha').value
  const response = await fetch('http://localhost:5000/predecir?fecha=' + fecha)
  const datos = await response.json()

  const responseHumedad = await fetch('http://localhost:5000//predecir_humedad?fecha=' + fecha)
  const datosHumedad = await responseHumedad.json()

  const reponseTemperatura = await fetch('http://localhost:5000/predecir_temperatura?fecha=' + fecha)
  const datosTemperatura = await reponseTemperatura.json()

  if (datosTemperatura.error) {
    alert(datosTemperatura.error)
    return
  }

  if (datosHumedad.error) {
    alert(datosHumedad.error)
    return
  }

  if (datos.error) {
    alert(datos.error)
    return
  }

  document.getElementById('resultadoTemperaturaIA').textContent = `${datosTemperatura.iowa.max.toFixed(2)}°F`
  document.getElementById('resultadoTemperaturaTX').textContent = `${datosTemperatura.texas.max.toFixed(2)}°F`
  document.getElementById('resultadoTemperaturaMO').textContent = `${datosTemperatura.missouri.max.toFixed(2)}°F`

  document.getElementById('resultadoHumedadTX').textContent = `${datosHumedad.texas.toFixed(2)}%`
  document.getElementById('resultadoHumedadMO').textContent = `${datosHumedad.missouri.toFixed(2)}%`
  document.getElementById('resultadoHumedadIA').textContent = `${datosHumedad.iowa.toFixed(2)}%`

  document.getElementById('resultadoIA').textContent = `${datos.prediccion_IA.toFixed(2)}%`
  document.getElementById('resultadoTX').textContent = `${datos.prediccion_TX.toFixed(2)}%`
  document.getElementById('resultadoMO').textContent = `${datos.prediccion_MO.toFixed(2)}%`
})
