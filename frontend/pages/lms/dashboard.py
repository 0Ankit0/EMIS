"""
LMS Dashboard
"""
import streamlit as st
from utils.helpers import show_info

def show():
    """Display lms dashboard"""
    st.title("LMS Dashboard")
    show_info("Feature available")
