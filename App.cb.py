import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="BJT CB Virtual Lab", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("CB Lab Navigation")
page = st.sidebar.radio("Go to", ["Aim & Theory", "Virtual Experiment", "Quiz & Assessment"])

# --- PAGE 1: AIM & THEORY ---
if page == "Aim & Theory":
    st.header("Experiment: Common Base (CB) Characteristics")
    
    st.subheader("1. Aim")
    st.write("To study and plot the Input and Output characteristics of an NPN transistor in Common Base configuration.")
    
    st.subheader("2. Theory")
    st.markdown("""
    In a **Common Base** configuration:
    * **Input Characteristics:** Relation between Emitter Current ($I_E$) and Emitter-Base Voltage ($V_{EB}$) at constant Collector-Base Voltage ($V_{CB}$).
    * **Output Characteristics:** Relation between Collector Current ($I_C$) and Collector-Base Voltage ($V_{CB}$) at constant Emitter Current ($I_E$).
    * **Alpha ($\alpha$):** The current gain, defined as $I_C / I_E$. It is always slightly less than 1 (typically 0.95 to 0.99).
    """)
    st.info("Note: In CB mode, the input resistance is very low and the output resistance is very high.")

# --- PAGE 2: VIRTUAL EXPERIMENT ---
elif page == "Virtual Experiment":
    st.header("CB Virtual Lab Setup")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Controls")
        alpha = st.slider("Set Current Gain (α)", 0.90, 0.99, 0.98, step=0.01)
        mode = st.selectbox("Select Characteristic", ["Input (Ie vs Veb)", "Output (Ic vs Vcb)"])
        
    if mode == "Input (Ie vs Veb)":
        v_cb_fix = st.sidebar.slider("Constant Vcb (V)", 0, 10, 2)
        v_eb = np.array([0, 0.1, 0.3, 0.5, 0.6, 0.7, 0.75, 0.8])
        # Model: Ie rises sharply after 0.7V
        i_e = np.where(v_eb > 0.6, (v_eb - 0.6) * 20, 0) # in mA
        
        df = pd.DataFrame({"Veb (V)": v_eb, "Ie (mA)": i_e})
        
        with col2:
            st.write(f"### Input Plot (Vcb = {v_cb_fix}V)")
            fig, ax = plt.subplots()
            ax.plot(v_eb, i_e, 'go-')
            ax.set_xlabel("Veb (Volts)")
            ax.set_ylabel("Ie (milliAmps)")
            ax.grid(True)
            st.pyplot(fig)
            st.table(df)

    else:
        i_e_fix = st.slider("Constant Ie (mA)", 1, 10, 5)
        v_cb = np.array([-1, 0, 1, 2, 4, 6, 8, 10])
        # Model: Ic is almost equal to Ie and stays constant
        i_c = alpha * i_e_fix * (1 + v_cb*0.001) # Very slight slope due to Early effect
        i_c = np.where(v_cb < 0, i_c * np.exp(v_cb), i_c) # Cutoff/Saturation dip

        df = pd.DataFrame({"Vcb (V)": v_cb, "Ic (mA)": i_c})

        with col2:
            st.write(f"### Output Plot (Ie = {i_e_fix}mA)")
            fig, ax = plt.subplots()
            ax.plot(v_cb, i_c, 'mo-')
            ax.set_xlabel("Vcb (Volts)")
            ax.set_ylabel("Ic (milliAmps)")
            ax.grid(True)
            st.pyplot(fig)
            st.table(df)

    st.divider()
    report_text = f"CB Lab Report\nMode: {mode}\nAlpha: {alpha}\nData Table:\n{df.to_string()}"
    st.download_button("Download CB Lab Report", report_text, file_name="cb_report.txt")

# --- PAGE 3: QUIZ ---
elif page == "Quiz & Assessment":
    st.header("CB Post-Lab Quiz")
    q1 = st.radio("1. What is the typical value of Current Gain (Alpha) in CB configuration?", ["Greater than 100", "Exactly 1", "Less than 1"])
    if st.button("Submit Quiz"):
        if q1 == "Less than 1":
            st.success("Correct! Alpha is usually between 0.95 and 0.99.")
        else:
            st.error("Incorrect. Remember, Ic = Alpha * Ie, and Ic is always slightly less than Ie.")
