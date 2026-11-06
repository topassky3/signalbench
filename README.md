# SignalBench: demostrador inicial

Prototipo numérico preparado para respaldar la propuesta a Hacker Initiative. **No es una validación de laboratorio y no contiene capturas de un receptor real.**

Requiere Python 3.10+ y NumPy. Instalar NumPy en un entorno virtual si no está disponible.

```bash
python -m unittest -v
python signalbench.py demo --out demo_output
python signalbench.py analyze demo_output/clean.sigmf-meta
```

El ensayo produce cuatro grabaciones sintéticas con metadatos SigMF básicos y un resumen JSON. Ilustra tono conocido, atenuación de amplitud, componente DC, recorte en los raíles y un error deliberado en la tasa de muestreo. La lectura admite datos vecinos `cf32_le` y `cu8`, un canal y desplazamiento cero. No se declara compatibilidad con todas las extensiones de SigMF.

La densidad espectral usa una ventana Hann y normalización por la energía de la ventana. La potencia se expresa respecto a una unidad de potencia media de muestra compleja; no es potencia RF calibrada en dBm. La frecuencia depende de la tasa de muestreo declarada. Un hash comprueba la integridad de los bytes contra un valor esperado; no demuestra su procedencia física ni que una medición sea verdadera.

Los seis controles comprueban invariantes numéricos e integridad de archivos. No miden exactitud, sensibilidad, rango dinámico, calibración o funcionamiento de un instrumento físico.

Próximo paso experimental: capturar un tono de referencia mediante conexión por cable y atenuación adecuada, repetir con tres ganancias y comparar contra la referencia. Conservar los bytes originales y publicar únicamente señales de banco que se puedan compartir.

Código bajo licencia MIT. Los escenarios sintéticos del demostrador se pueden regenerar con la semilla incluida.

Referencias: https://sigmf.org/ y https://www.gnuradio.org/about/.
