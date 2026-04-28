Quiero crear una aplicación en Python usando Streamlit.

El objetivo es hacer una app muy sencilla para personas mayores que les ayude a gestionar sus medicamentos.

REQUISITOS DE DISEÑO (MUY IMPORTANTE):

* Todo debe estar en una sola pantalla (sin navegación entre páginas)
* Interfaz extremadamente simple
* Botones muy grandes y fáciles de pulsar
* Texto grande y legible (pensado para personas mayores)
* Alto contraste (fondo claro, texto oscuro)
* Cada acción debe tener icono + texto (por ejemplo: 💊, ➕, 🛒)
* Evitar saturación visual (muy limpio)

FUNCIONALIDAD DE LA PANTALLA PRINCIPAL:

1. Título arriba: “💊 Mis medicamentos”
2. Botón grande: “➕ Añadir medicamento”
3. Debajo, lista de medicamentos visibles directamente (sin hacer clic)

Cada medicamento debe mostrarse como una tarjeta clara con:

* Nombre del medicamento (grande)
* Dosis (ej: mañana / noche)
* Cantidad restante

Cada medicamento debe tener dos botones grandes:

* ✔️ Tomado
* 🛒 Comprar

COMPORTAMIENTO:

* No usar navegación ni múltiples páginas
* Todo debe actualizarse en la misma pantalla
* Usar st.session_state para guardar los medicamentos
* El código debe ser limpio y fácil de entender

EXTRA:

* Añadir separadores visuales entre medicamentos
* Que se vea bien tanto en ordenador como en móvil (diseño vertical)

Devuélveme SOLO el código en Python usando Streamlit, listo para copiar y ejecutar.
