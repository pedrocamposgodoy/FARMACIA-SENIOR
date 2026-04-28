import streamlit as st
from datetime import datetime
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gestión de Medicamentos", page_icon="💊", layout="wide")

# --- ESTILOS CSS AVANZADOS ---
st.markdown("""
    <style>
    /* Estilos globales y utilidades */
    .big-font { font-size: 20px !important; }
    
    /* Tarjetas para el Modo Senior */
    .senior-card {
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        background-color: #ffffff;
    }
    .senior-card.ok { border-left: 10px solid #198754; }
    .senior-card.pending { border-left: 10px solid #ffc107; background-color: #fffdf5; }
    
    .senior-title { font-size: 32px; font-weight: 800; color: #212529; margin-bottom: 10px; }
    .senior-subtitle { font-size: 24px; color: #495057; margin-bottom: 20px; }
    
    /* Botones gigantes Modo Senior */
    div[data-testid="stButton"] button {
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .senior-btn div[data-testid="stButton"] button {
        height: 90px !important;
        width: 100% !important;
        font-size: 28px !important;
        background-color: #0d6efd;
        color: white;
        border: none;
    }
    .senior-btn div[data-testid="stButton"] button:hover {
        background-color: #0b5ed7;
        transform: scale(1.02);
    }
    
    /* Tarjetas de Búsqueda CIMA/Vademecum */
    .cima-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 10px;
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MOCK (st.session_state) ---
if 'db' not in st.session_state:
    st.session_state.db = [
        {
            "id": "1", "nombre": "Paracetamol 1g", "principio_activo": "Paracetamol",
            "dosis": "Mañana", "stock_actual": 8, "stock_inicial": 20, 
            "necesita_receta": False, "tomado_hoy": False, "ultima_toma": None,
            "prospecto_url": "https://cima.aemps.es/cima/pdfs/p/70081/P_70081.pdf",
            "advertencias": ["Evitar alcohol"]
        },
        {
            "id": "2", "nombre": "Enalapril 20mg", "principio_activo": "Enalapril maleato",
            "dosis": "Noche", "stock_actual": 25, "stock_inicial": 30, 
            "necesita_receta": True, "tomado_hoy": True, "ultima_toma": "08:30",
            "prospecto_url": "https://cima.aemps.es/cima/pdfs/p/60555/P_60555.pdf",
            "advertencias": ["Precaución al conducir"]
        }
    ]

# --- SIMULADOR API AEMPS / VADEMECUM ---
def buscar_en_cima(query):
    """Simula una llamada REST a la API de medicamentos del gobierno"""
    resultados_mock = [
        {"nombre": "Sintrom 4mg", "principio": "Acenocumarol", "receta": True, "prospecto": "https://cima.aemps.es/cima/pdfs/es/p/26456/P_26456.pdf", "adv": ["Control médico estricto"]},
        {"nombre": "Ibuprofeno 600mg", "principio": "Ibuprofeno", "receta": True, "prospecto": "https://cima.aemps.es/cima/pdfs/es/p/65301/P_65301.pdf", "adv": ["Tomar con alimentos"]},
        {"nombre": "Omeprazol 20mg", "principio": "Omeprazol", "receta": False, "prospecto": "https://cima.aemps.es/cima/pdfs/es/p/63012/P_63012.pdf", "adv": []}
    ]
    # Filtrado simple para la demo
    return [r for r in resultados_mock if query.lower() in r['nombre'].lower() or query.lower() in r['principio'].lower()]

# --- CONTROL DE NAVEGACIÓN (BARRA LATERAL) ---
with st.sidebar:
    st.title("⚙️ Panel de Control")
    vista_actual = st.radio("Seleccionar Interfaz:", ["👴 Pantalla Senior", "🏠 Gestión Familiar"], label_visibility="collapsed")
    st.markdown("---")
    st.info("**Aviso Legal:** Información extraída de fuentes oficiales. No sustituye consejo médico.")

# ==========================================
# VISTA 1: MODO SENIOR (ALTA ACCESIBILIDAD)
# ==========================================
if vista_actual == "👴 Pantalla Senior":
    st.title(f"📅 Mis Medicamentos - {datetime.now().strftime('%d/%m/%Y')}")
    st.write("") # Espaciador
    
    if no st.session_state.db:
        st.info("No hay medicamentos programados para hoy.")
        
    for i, med in enumerate(st.session_state.db):
        estado_css = "ok" if med['tomado_hoy'] else "pending"
        icono_estado = "✅ TOMADO" if med['tomado_hoy'] else "⏳ PENDIENTE"
        
        # Tarjeta visual
        st.markdown(f"""
            <div class="senior-card {estado_css}">
                <div class="senior-title">💊 {med['nombre']}</div>
                <div class="senior-subtitle">🕒 Toca por la <b>{med['dosis']}</b></div>
                <div style="font-size: 1.2rem; color: #6c757d;">Estado: {icono_estado}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Lógica del botón de toma
        if not med['tomado_hoy']:
            st.markdown('<div class="senior-btn">', unsafe_allow_html=True)
            if st.button(f"✔️ CONFIRMAR TOMA: {med['nombre']}", key=f"toma_{i}"):
                if med['stock_actual'] > 0:
                    st.session_state.db[i]['stock_actual'] -= 1
                    st.session_state.db[i]['tomado_hoy'] = True
                    st.session_state.db[i]['ultima_toma'] = datetime.now().strftime("%H:%M")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success(f"🎉 ¡Perfecto! Registrado a las {med['ultima_toma']}")
            
        st.write("") # Espaciador

# ==========================================
# VISTA 2: GESTIÓN FAMILIAR (BACKOFFICE)
# ==========================================
else:
    st.title("📊 Panel de Gestión Familiar")
    
    # 1. DASHBOARD DE MÉTRICAS (Fase 1 y 3)
    st.subheader("Resumen de Adherencia e Inventario")
    col1, col2, col3, col4 = st.columns(4)
    
    total_meds = len(st.session_state.db)
    tomas_completadas = sum(1 for m in st.session_state.db if m['tomado_hoy'])
    stock_bajo = sum(1 for m in st.session_state.db if m['stock_actual'] < (m['stock_inicial'] * 0.2)) # Alerta si < 20%
    recetas_activas = sum(1 for m in st.session_state.db if m['necesita_receta'])
    
    col1.metric("Progreso Diario", f"{tomas_completadas} / {total_meds}", "Tomas completadas")
    col2.metric("Alertas de Farmacia", stock_bajo, "A reponer" if stock_bajo > 0 else "OK", delta_color="inverse")
    col3.metric("Con Receta 🩺", recetas_activas)
    col4.metric("Total Tratamientos", total_meds)
    
    st.markdown("---")
    
    # PESTAÑAS DE GESTIÓN (Organización de Fase 2 y 4)
    tab1, tab2, tab3 = st.tabs(["📦 Inventario y Fichas", "➕ Vademecum (Añadir)", "🔄 Reiniciar Día"])
    
    # --- TAB 1: INVENTARIO DETALLADO ---
    with tab1:
        for i, med in enumerate(st.session_state.db):
            with st.expander(f"{'🔴' if med['stock_actual'] < 5 else '🟢'} {med['nombre']} - Quedan {med['stock_actual']} pastillas"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.write(f"**Principio Activo:** {med['principio_activo']}")
                    st.write(f"**Pauta:** {med['dosis']}")
                    
                    # Barra de progreso de stock
                    porcentaje_stock = max(min(med['stock_actual'] / med['stock_inicial'], 1.0), 0.0)
                    color_barra = "green" if porcentaje_stock > 0.3 else ("yellow" if porcentaje_stock > 0.1 else "red")
                    st.progress(porcentaje_stock, text=f"Nivel de caja: {med['stock_actual']}/{med['stock_inicial']}")
                    
                    if med['advertencias']:
                        st.warning(f"⚠️ **Precauciones:** {', '.join(med['advertencias'])}")
                
                with c2:
                    if med['necesita_receta']:
                        st.error("🩺 Requiere Receta Médica")
                    if med['prospecto_url']:
                        st.markdown(f"[📥 Descargar Prospecto Oficial (PDF)]({med['prospecto_url']})")
                        
                    # Botón para reponer stock
                    if st.button("🛒 Registrar compra en farmacia", key=f"compra_{i}"):
                        st.session_state.db[i]['stock_actual'] += med['stock_inicial']
                        st.rerun()

    # --- TAB 2: BUSCADOR VADEMECUM (INTEGRACIÓN) ---
    with tab2:
        st.write("### Buscar en la Base de Datos Oficial (AEMPS)")
        query = st.text_input("🔍 Introduce el nombre comercial o principio activo:", placeholder="Ej: Sintrom, Ibuprofeno...")
        
        if query:
            resultados = buscar_en_cima(query)
            if resultados:
                for res in resultados:
                    st.markdown(f"""
                        <div class="cima-card">
                            <h4>{res['nombre']} <span style="font-size:14px; font-weight:normal;">({res['principio']})</span></h4>
                            <p>{'🩺 Con receta' if res['receta'] else '🟢 Sin receta'} | <a href="{res['prospecto']}" target="_blank">Ver prospecto</a></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Formulario de configuración rápida para añadirlo
                    with st.form(key=f"form_{res['nombre']}"):
                        col_a, col_b = st.columns(2)
                        dosis_nueva = col_a.selectbox("Frecuencia de toma", ["Mañana", "Mediodía", "Noche", "Cada 8h"], key=f"dosis_{res['nombre']}")
                        stock_nuevo = col_b.number_input("Pastillas en la caja", min_value=1, value=30, key=f"stock_{res['nombre']}")
                        
                        if st.form_submit_button("➕ Añadir al botiquín del paciente"):
                            nuevo_med = {
                                "id": str(len(st.session_state.db) + 1),
                                "nombre": res['nombre'],
                                "principio_activo": res['principio'],
                                "dosis": dosis_nueva,
                                "stock_actual": stock_nuevo,
                                "stock_inicial": stock_nuevo,
                                "necesita_receta": res['receta'],
                                "tomado_hoy": False,
                                "ultima_toma": None,
                                "prospecto_url": res['prospecto'],
                                "advertencias": res['adv']
                            }
                            st.session_state.db.append(nuevo_med)
                            st.success(f"¡{res['nombre']} añadido al plan del paciente!")
                            st.rerun()
            else:
                st.warning("No se encontraron resultados en la base de datos para esa búsqueda.")

    # --- TAB 3: CONTROL TÉCNICO ---
    with tab3:
        st.write("### Mantenimiento Diario")
        st.info("Esta acción simula el cambio de día, reiniciando los marcadores de las tomas a 'Pendiente'.")
        if st.button("🔄 Reiniciar tomas para un nuevo día"):
            for med in st.session_state.db:
                med['tomado_hoy'] = False
                med['ultima_toma'] = None
            st.success("Día reiniciado. Las tarjetas volverán a estar pendientes en la Pantalla Senior.")
            st.rerun()
