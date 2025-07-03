import streamlit as st
import pandas as pd

def show_state(state = "////////////////////////////////////"):
    if len(state) != 36:
        st.error("String length must equal 36!")
    
    st.title("demo UI")

    cells = {
        '/':'⬜',
        'a':'🟧',
        'b':'🟦',
        'c':'🟦',
        # reserved space
        'm':'🟨',
        'n':'🟨'
    }

    st.markdown("### UI_1:")
    bstr = ""
    for i in range(36):
        if i % 6 == 0:
            bstr += '\n'
        bstr += cells.get(state[i], '❌')
    
    st.markdown(f"```{bstr}\n```")

show_state("/////////////a/////////////////m////")