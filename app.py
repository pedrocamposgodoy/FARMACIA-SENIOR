import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="💊 Mis Medicamentos",
    page_icon="💊",
    layout="centered"
)

# CSS personalizado para diseño adaptado a personas mayores
st.markdown("""
<style>
    /* Fondo claro y texto oscuro */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Título principal */
    h1 {
        font-size: 3rem !important;
        color: #1a1a1a !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Botones grandes */
    .stButton > button {
        font-size: 1.8rem !important;
        padding: 1.5rem 3rem !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Inputs de texto grandes */
    input {
        font-size: 1.5rem !important;
        padding: 1rem !important;
    }
    
    /* Selectbox grande */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #1a1a1a !important;
    }
    
    /* Tarjetas de medicamentos */
    .medicamento-card {
        background-color: #f8f9fa;
        border: 3px solid #dee2e6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .med-nombre {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .med-info {
        font-size: 1.5rem;
        color: #495057;
        margin: 0.5rem 0;
    }
    
    .med-cantidad {
        font-size: 1.6rem;
        font-weight: bold;
        color: #dc3545;
        margin: 0.5rem 0;
    }
    
    .med-cantidad-ok {
        color: #28a745;
    }
    
    /* Separador */
    hr {
        border: 2px solid #dee2e6;
        margin: 2rem 0;
    }
    
    /* Mensajes de éxito/info */
    .stSuccess, .stInfo {
        font-size: 1.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session_state
if 'medicamentos' not in st.session_state:
    st.session_state.medicamentos = []

if 'mostrar_formulario' not in st.session_state:
    st.session_state.mostrar_formulario = False

# Función para añadir medicamento
def agregar_medicamento(nombre, dosis, cantidad):
    medicamento = {
        'nombre': nombre,
        'dosis': dosis,
        'cantidad': cantidad,
        'id': datetime.now().timestamp()
    }
    st.session_state.medicamentos.append(medicamento)
    st.session_state.mostrar_formulario = False

# Función para marcar como tomado
def marcar_tomado(med_id):
    for med in st.session_state.medicamentos:
        if med['id'] == med_id:
            if med['cantidad'] > 0:
                med['cantidad'] -= 1

# Función para eliminar medicamento
def eliminar_medicamento(med_id):
    st.session_state.medicamentos = [m for m in st.session_state.medicamentos if m['id'] != med_id]

# PANTALLA PRINCIPAL
st.title("💊 Mis Medicamentos")

# Botón para mostrar/ocultar formulario
if not st.session_state.mostrar_formulario:
    if st.button("➕ Añadir Medicamento", type="primary"):
        st.session_state.mostrar_formulario = True
        st.rerun()
else:
    # Formulario para añadir medicamento
    st.markdown("---")
    st.markdown("### ➕ Nuevo Medicamento")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        nombre = st.text_input("Nombre del medicamento", placeholder="Ej: Paracetamol")
        
        dosis = st.selectbox(
            "¿Cuándo lo tomas?",
            ["Mañana", "Mediodía", "Noche", "Mañana y Noche", "Cada 8 horas"]
        )
        
        cantidad = st.number_input("¿Cuántas pastillas tienes?", min_value=0, value=30, step=1)
    
    col_guardar, col_cancelar = st.columns(2)
    
    with col_guardar:
        if st.button("✅ Guardar", type="primary"):
            if nombre:
                agregar_medicamento(nombre, dosis, cantidad)
                st.success(f"✅ {nombre} añadido correctamente")
                st.rerun()
            else:
                st.error("⚠️ Por favor, escribe el nombre del medicamento")
    
    with col_cancelar:
        if st.button("❌ Cancelar"):
            st.session_state.mostrar_formulario = False
            st.rerun()
    
    st.markdown("---")

# LISTA DE MEDICAMENTOS
if len(st.session_state.medicamentos) > 0:
    st.markdown("---")
    st.markdown("### 📋 Mis Medicamentos")
    
    for med in st.session_state.medicamentos:
        # Determinar color según cantidad
        clase_cantidad = "med-cantidad-ok" if med['cantidad'] > 10 else ""
        
        st.markdown(f"""
        <div class="medicamento-card">
            <div class="med-nombre">💊 {med['nombre']}</div>
            <div class="med-info">🕐 {med['dosis']}</div>
            <div class="med-cantidad {clase_cantidad}">
                📦 Quedan: {med['cantidad']} pastillas
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button(f"✔️ Tomado", key=f"tomado_{med['id']}", type="primary"):
                if med['cantidad'] > 0:
                    marcar_tomado(med['id'])
                    st.success(f"✅ Tomaste {med['nombre']}")
                    st.rerun()
                else:
                    st.error("⚠️ No quedan pastillas")
        
        with col2:
            if st.button(f"🛒 Comprar", key=f"comprar_{med['id']}"):
                st.info(f"🛒 Recuerda comprar {med['nombre']}")
        
        with col3:
            if st.button(f"🗑️", key=f"eliminar_{med['id']}", help="Eliminar medicamento"):
                eliminar_medicamento(med['id'])
                st.rerun()
        
        st.markdown("---")
else:
    if not st.session_state.mostrar_formulario:
        st.info("📝 No tienes medicamentos registrados. Pulsa **➕ Añadir Medicamento** para empezar.")

# Pie de página
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; font-size: 1.2rem; padding: 1rem;'>
    💡 Consejo: Pulsa <b>✔️ Tomado</b> cada vez que tomes tu medicamento
</div>
""", unsafe_allow_html=True)
