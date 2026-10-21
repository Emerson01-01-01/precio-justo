import streamlit as st
import pandas as pd
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Radar de Precios - INNOVaiLAB", page_icon="📈", layout="wide")

# --- CSS PERSONALIZADO PARA DARLE UN LOOK "FINTECH" ---
st.markdown("""
<style>
    .main-title { font-size: 40px; color: #075E54; font-weight: 900; }
    .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #075E54; }
    .alert-red { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; font-weight: bold; }
    .alert-green { background-color: #00cc66; color: white; padding: 15px; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📈 Radar de Precios</p>', unsafe_allow_html=True)
st.markdown("**Empoderando a los vendedores de Riobamba con inteligencia de mercado en tiempo real.**")

# --- DATOS SIMULADOS (Base de Datos) ---
# En el hackathon, esto puede ser un CSV que actualices.
data = {
    "Producto": ["Papa", "Tomate", "Cebolla", "Zanahoria", "Aguacate"],
    "Precio Mínimo": [0.40, 0.50, 0.35, 0.25, 0.80],
    "Precio Máximo": [0.60, 0.75, 0.50, 0.40, 1.20],
    "Costo Promedio": [0.25, 0.35, 0.20, 0.15, 0.50],
    "Tendencia": ["📉 Bajando", "📈 Subiendo", "➡️ Estable", "📈 Subiendo", "📉 Bajando"]
}
df = pd.DataFrame(data)

# --- SECCIÓN 1: EL SEMÁFORO DE MERCADO ---
st.markdown("### 🚦 Semáforo de Mercado (Hoy)")
st.write("Te mostramos si es buen momento para vender tus productos según los datos locales.")

cols = st.columns(len(df))
for idx, row in df.iterrows():
    with cols[idx]:
        # Lógica del semáforo: si el margen es menor al 30%, es alerta roja.
        margen = (row['Precio Mínimo'] - row['Costo Promedio']) / row['Precio Mínimo']
        
        if margen < 0.30:
            status = "🔴 RIESGO"
            css_class = "alert-red"
            msg = "Margen bajo. ¡No vendas a menos de ${:.2f}!".format(row['Precio Mínimo'])
        else:
            status = "🟢 OPORTUNIDAD"
            css_class = "alert-green"
            msg = "Buen margen. Pide hasta ${:.2f}".format(row['Precio Máximo'])
            
        st.markdown(f"**{row['Producto']}**")
        st.markdown(f"<div class='{css_class}' style='font-size:14px;'>{status}<br>{msg}</div>", unsafe_allow_html=True)
        st.caption(f"Tendencia: {row['Tendencia']}")

st.divider()

# --- SECCIÓN 2: CALCULADORA VISUAL (El "Wow" Factor) ---
st.markdown("### 🧮 Calculadora de Ganancia Real")
st.write("Ajusta tus costos y mira cómo cambia tu ganancia. **No aceptes ofertas por debajo de la línea verde.**")

col1, col2 = st.columns([1, 2])

with col1:
    producto_sel = st.selectbox("Selecciona tu producto", df["Producto"])
    cantidad = st.number_input("¿Cuántas libras/unidades tienes?", min_value=1, value=100, step=10)
    
    # Obtener datos del producto seleccionado
    prod_data = df[df["Producto"] == producto_sel].iloc[0]
    
    costo_real = st.slider("¿Cuánto te costó producir/comprar (por unidad)?", 
                           min_value=0.0, max_value=float(prod_data['Precio Máximo']), 
                           value=float(prod_data['Costo Promedio']), step=0.01)
    
    precio_oferta = st.slider("¿A cuánto te quieren comprar (oferta)?", 
                              min_value=0.0, max_value=float(prod_data['Precio Máximo'] * 1.5), 
                              value=float(prod_data['Precio Mínimo']), step=0.01)

with col2:
    # Cálculos
    ingreso_total = cantidad * precio_oferta
    costo_total = cantidad * costo_real
    ganancia_neta = ingreso_total - costo_total
    
    # Mostrar métricas grandes
    st.markdown("#### 📊 Resultados Proyectados")
    st.metric(label="Ingreso Total", value=f"${ingreso_total:,.2f}")
    st.metric(label="Costo Total", value=f"${costo_total:,.2f}")
    
    if ganancia_neta < 0:
        st.metric(label="Ganancia Neta", value=f"-${abs(ganancia_neta):,.2f}", delta="¡ESTÁS PERDIENDO DINERO!", delta_color="inverse")
        st.error("🚨 **ALERTA:** Esta oferta te hace perder dinero. Exige un precio mayor.")
    elif ganancia_neta < (costo_total * 0.3):
        st.metric(label="Ganancia Neta", value=f"${ganancia_neta:,.2f}", delta="Margen muy bajo", delta_color="off")
        st.warning("⚠️ **Cuidado:** Tu margen es menor al 30%. Estás trabajando casi gratis.")
    else:
        st.metric(label="Ganancia Neta", value=f"${ganancia_neta:,.2f}", delta="¡Buen margen!", delta_color="normal")
        st.success("✅ **¡Excelente!** Esta es una oferta justa. Puedes negociar con confianza.")

    # Generador de "Pase de Venta" (Simulado)
    if st.button("📄 Generar Pase de Venta (Para mostrar al comprador)", use_container_width=True):
        with st.spinner("Generando documento..."):
            time.sleep(1)
            st.info(f"""
            **PASE DE VENTA - RADAR DE PRECIOS**  
            **Producto:** {producto_sel}  
            **Cantidad:** {cantidad}  
            **Precio Justo de Mercado:** ${prod_data['Precio Mínimo']:.2f} - ${prod_data['Precio Máximo']:.2f}  
            **Tu Oferta:** ${precio_oferta:.2f}  
            
            *Este documento certifica que el precio ofrecido está dentro del rango del mercado. ¡Exige un trato justo!*
            """)
