"""
Loading Components
"""
import streamlit as st
import time
from typing import Optional


def show_spinner(message: str = "Loading..."):
    """Show loading spinner"""
    return st.spinner(message)


def show_progress_bar(progress: float, text: Optional[str] = None):
    """
    Show progress bar
    progress: 0.0 to 1.0
    """
    if text:
        st.text(text)
    st.progress(progress)


def show_loading_animation(duration: int = 3, message: str = "Processing..."):
    """Show loading animation with progress"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(duration * 10):
        progress = (i + 1) / (duration * 10)
        progress_bar.progress(progress)
        status_text.text(f"{message} {int(progress * 100)}%")
        time.sleep(0.1)
    
    progress_bar.empty()
    status_text.empty()


def show_skeleton_loader(num_rows: int = 3):
    """Show skeleton loader for table data"""
    for _ in range(num_rows):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.empty()
        with col2:
            st.empty()
        with col3:
            st.empty()
