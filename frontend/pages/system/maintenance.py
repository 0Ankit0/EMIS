"""
Maintenance Mode
"""
import streamlit as st
from utils.helpers import show_info

def show():
    """Display maintenance mode"""
    st.title("Maintenance Mode")
    show_info("Feature available")
