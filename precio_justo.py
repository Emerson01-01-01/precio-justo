import streamlit as st
import re
import time

# --- CONFIGURACIÓN VISUAL (Simulando WhatsApp) ---
st.set_page_config(page_title="Precio Justo - INNOVaiLAB", page_icon="💸", layout="centered")

st.markdown("""
<style>
    /* Estilos para simular WhatsApp */
    .whatsapp-header {
        background-color: #075E54; 
        color: white; 
        padding: 15px; 
        border-radius: 10px 10px 0 0; 
        text-align: center; 
        font-weight: bold;
        font-size: 20px;
        margin-bottom: -10px;
    }
    .stChatMessage { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="whatsapp-header">💸 Precio Justo<br><span style="font-size:12px; font-weight:normal;">Tu asistente de ventas con IA</span></div>', unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL (Precios de Mercado de Riobamba) ---
# IMPORTANTE: Actualiza estos precios mañana si puedes preguntar en el mercado.
# Estructura: "producto": {"precio_min": X, "precio_max": Y}
PRECIOS_MERCADO = {
    "papa": {"precio_min": 0.40, "precio_max": 0.60, "unidad": "libra"},
    "tomate": {"precio_min": 0.50, "precio_max": 0.75, "unidad": "libra"},
    "cebolla": {"precio_min": 0.35, "precio_max": 0.50, "unidad": "libra"},
    "zanahoria": {"precio_min": 0.25, "precio_max": 0.40, "unidad": "libra"},
    "aguacate": {"precio_min": 0.80, "precio_max": 1.20, "unidad": "unidad"},
    "pollo": {"precio_min": 2.50, "precio_max": 3.20, "unidad": "libra"}
}

# --- LÓGICA DE EXTRACCIÓN (Simulando IA) ---
def extraer_datos(mensaje):
    """Extrae producto, cantidad y costo del mensaje del usuario usando expresiones regulares."""
    mensaje = mensaje.lower()
    producto_encontrado = None
    cantidad = None
    costo_unitario = None

    # 1. Buscar el producto
    for prod in PRECIOS_MERCADO.keys():
        if prod in mensaje:
            producto_encontrado = prod
            break
    
    # 2. Buscar cantidad (números que no tengan un punto decimal antes, para evitar agarrar el costo)
    cantidades = re.findall(r'\b(\d+)\b', mensaje)
    if cantidades:
        cantidad = int(cantidades[0])

    # 3. Buscar costo (números con decimal, o palabras clave como "costo", "compre a")
    match_costo = re.search(r'(?:costo|compre a|a)\s*\$?(\d+[.,]\d+)', mensaje)
    if match_costo:
        costo_unitario = float(match_costo.group(1).replace(',', '.'))
    else:
        # Si no encuentra el costo explícito, asumimos un costo estimado del 60% del precio mínimo
        if producto_encontrado:
            costo_unitario = PRECIOS_MERCADO[producto_encontrado]["precio_min"] * 0.6

    return producto_encontrado, cantidad, costo_unitario

# --- GENERADOR DE RESPUESTAS ---
def generar_respuesta(mensaje):
    producto, cantidad, costo = extraer_datos(mensaje)
    
    if not producto:
        return "🤔 No reconocí el producto. Prueba con: papa, tomate, cebolla, zanahoria, aguacate o pollo.\n\n*Ejemplo:* 'Tengo 100 papas, me costaron 0.30'"
    
    if not cantidad:
        cantidad = 10 # Valor por defecto si no dice cantidad
    
    datos_mercado = PRECIOS_MERCADO[producto]
    p_min = datos_mercado["precio_min"]
    p_max = datos_mercado["precio_max"]
    
    # Cálculos
    ingreso_min = p_min * cantidad
    ingreso_max = p_max * cantidad
    costo_total = (costo or 0) * cantidad if costo else 0
    ganancia_min = ingreso_min - costo_total
    ganancia_max = ingreso_max - costo_total

    # Construir respuesta con formato de WhatsApp (*negrita*)
    respuesta = f"📦 *Análisis para {cantidad} {datos_mercado['unidad']}s de {producto}:*\n\n"
    respuesta += f"📊 *Precio justo en el mercado:*\n"
    respuesta += f"   • Mínimo: ${p_min:.2f}\n"
    respuesta += f"   • Máximo: ${p_max:.2f}\n\n"
    
    if costo:
        respuesta += f"💵 Tu costo total: ${costo_total:.2f}\n"
        respuesta += f"💰 *Ganancia estimada:*\n"
        respuesta += f"   • Si vendes barato: ${ganancia_min:.2f}\n"
        respuesta += f"   • Si vendes bien: ${ganancia_max:.2f}\n\n"
        
        if ganancia_min < 0:
            respuesta += "🚨 *¡ALERTA!* Estás vendiendo a pérdida. Sube tu precio a por lo menos $" + f"{p_min:.2f} para no perder dinero."
        else:
            respuesta += "✅ *Consejo:* Intenta vender cerca del precio máximo. ¡No regales tu trabajo!"
    else:
        respuesta += "💡 *Consejo:* Dime cuánto te costó (ej: 'me costó 0.30') para calcular tu ganancia exacta."

    return respuesta

# --- INTERFAZ DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente *Precio Justo* 🤖. Dime qué vas a vender y cuánto te costó.\n\n*Ejemplo:* 'Tengo 100 papas, me costaron 0.25'"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analizando precios... ⏳")
        time.sleep(0.8) # Simula el tiempo de respuesta de la IA
        
        respuesta_final = generar_respuesta(prompt)
        message_placeholder.markdown(respuesta_final)
    
    st.session_state.messages.append({"role": "assistant", "content": respuesta_final})