import matplotlib
matplotlib.use('Agg')  # Required for web server stability
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Page Config
st.set_page_config(page_title="BJT Virtual Lab", layout="wide")

# --- NAVIGATION ---
st.sidebar.title("Laboratory Menu")
lab_type = st.sidebar.selectbox("Select Experiment", ["Common Emitter (CE)", "Common Base (CB)"])
page = st.sidebar.radio("Navigation", ["Theory", "Virtual Experiment", "Quiz"])

# --- COMMON EMITTER (CE) LOGIC ---
if lab_type == "Common Emitter (CE)":
    if page == "Theory":
        st.header("Theory: Common Emitter Configuration")
        st.write("In CE configuration, the **Emitter** is common to both input and output.")
        st.markdown("""
        - **Input:** $V_{BE}$ vs $I_B$ (at constant $V_{CE}$)
        - **Output:** $V_{CE}$ vs $I_C$ (at constant $I_B$)
        - **Gain:** $\\beta = I_C / I_B$
        """)

    elif page == "Virtual Experiment":
        st.header("CE Characteristics Lab")
        mode = st.selectbox("Characteristic", ["Input (Ib vs Vbe)", "Output (Ic vs Vce)"])
        beta = st.slider("Current Gain (Beta)", 50, 200, 100)

        if mode == "Input (Ib vs Vbe)":
            v_be = np.linspace(0, 0.9, 10)
            i_b = np.where(v_be > 0.65, (v_be - 0.65) * 500, 0)
            df = pd.DataFrame({"Vbe (V)": v_be, "Ib (uA)": i_b})
            
            fig, ax = plt.subplots()
            ax.plot(v_be, i_b, 'ro-', label="Vce = 5V")
            ax.set_xlabel("Vbe (V)")
            ax.set_ylabel("Ib (uA)")
            ax.legend()
            st.pyplot(fig)
            st.table(df)

        else:
            ib_fix = st.select_slider("Constant Ib (uA)", [10, 20, 30, 40, 50])
            v_ce = np.array([0, 0.5, 1, 2, 4, 6, 8, 10])
            ic = (beta * ib_fix / 1000) * (1 - np.exp(-v_ce/0.5))
            df = pd.DataFrame({"Vce (V)": v_ce, "Ic (mA)": ic})

            fig, ax = plt.subplots()
            ax.plot(v_ce, ic, 'bo-', label=f"Ib = {ib_fix}uA")
            ax.set_xlabel("Vce (V)")
            ax.set_ylabel("Ic (mA)")
            ax.legend()
            st.pyplot(fig)
            st.table(df)

# --- COMMON BASE (CB) LOGIC ---
else:
    if page == "Theory":
        st.header("Theory: Common Base Configuration")
        st.write("In CB configuration, the **Base** is common to both input and output.")
        st.markdown("""
        - **Input:** $V_{EB}$ vs $I_E$ (at constant $V_{CB}$)
        - **Output:** $V_{CB}$ vs $I_C$ (at constant $I_E$)
        - **Gain:** $\\alpha = I_C / I_E$ (Always < 1)
        """)

    elif page == "Virtual Experiment":
        st.header("CB Characteristics Lab")
        mode = st.selectbox("Characteristic", ["Input (Ie vs Veb)", "Output (Ic vs Vcb)"])
        alpha = st.slider("Current Gain (Alpha)", 0.95, 0.99, 0.98)

        if mode == "Input (Ie vs Veb)":
            v_eb = np.linspace(0, 0.9, 10)
            i_e = np.where(v_eb > 0.65, (v_eb - 0.65) * 20, 0)
            df = pd.DataFrame({"Veb (V)": v_eb, "Ie (mA)": i_e})

            fig, ax = plt.subplots()
            ax.plot(v_eb, i_e, 'go-', label="Vcb = 2V")
            ax.set_xlabel("Veb (V)")
            ax.set_ylabel("Ie (mA)")
            ax.legend()
            st.pyplot(fig)
            st.table(df)

        else:
            ie_fix = st.select_slider("Constant Ie (mA)", [1, 2, 3, 4, 5])
            v_cb = np.array([0, 1, 2, 4, 6, 8, 10])
            ic = alpha * ie_fix * (1 + v_cb * 0.001)
            df = pd.DataFrame({"Vcb (V)": v_cb, "Ic (mA)": ic})

            fig, ax = plt.subplots()
            ax.plot(v_cb, ic, 'mo-', label=f"Ie = {ie_fix}mA")
            ax.set_xlabel("Vcb (V)")
            ax.set_ylabel("Ic (mA)")
            ax.legend()
            st.pyplot(fig)
            st.table(df)

# --- QUIZ SECTION ---
if page == "Quiz":
    st.header("Quick Assessment")
    q1 = st.radio("Which configuration provides the highest voltage gain?", ["Common Base", "Common Emitter", "Common Collector"])
    if st.button("Check Answer"):
        if q1 == "Common Emitter":
            st.success("Correct!")
        else:
            st.error("Incorrect. CE configuration provides high voltage and current gain.")
