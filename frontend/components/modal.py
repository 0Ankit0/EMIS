"""
Modal Dialog Components
"""
import streamlit as st
from typing import Callable, Optional


@st.experimental_dialog("Confirmation")
def show_confirmation_dialog(message: str, on_confirm: Callable, on_cancel: Optional[Callable] = None):
    """Show confirmation dialog"""
    st.write(message)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Confirm", type="primary", use_container_width=True):
            on_confirm()
            st.rerun()
    
    with col2:
        if st.button("Cancel", use_container_width=True):
            if on_cancel:
                on_cancel()
            st.rerun()


def show_alert_dialog(title: str, message: str, alert_type: str = "info"):
    """Show alert dialog"""
    with st.expander(f"⚠️ {title}", expanded=True):
        if alert_type == "success":
            st.success(message)
        elif alert_type == "error":
            st.error(message)
        elif alert_type == "warning":
            st.warning(message)
        else:
            st.info(message)


def show_form_dialog(title: str, fields: dict, on_submit: Callable):
    """
    Show form dialog
    fields: dict of field_name: field_type
    """
    with st.expander(f"📝 {title}", expanded=True):
        with st.form(key=f"dialog_form_{title}"):
            form_data = {}
            
            for field_name, field_config in fields.items():
                field_type = field_config.get("type", "text")
                label = field_config.get("label", field_name)
                required = field_config.get("required", False)
                
                if field_type == "text":
                    form_data[field_name] = st.text_input(
                        label,
                        key=f"{field_name}_input"
                    )
                elif field_type == "textarea":
                    form_data[field_name] = st.text_area(
                        label,
                        key=f"{field_name}_input"
                    )
                elif field_type == "number":
                    form_data[field_name] = st.number_input(
                        label,
                        key=f"{field_name}_input"
                    )
                elif field_type == "date":
                    form_data[field_name] = st.date_input(
                        label,
                        key=f"{field_name}_input"
                    )
                elif field_type == "select":
                    options = field_config.get("options", [])
                    form_data[field_name] = st.selectbox(
                        label,
                        options,
                        key=f"{field_name}_input"
                    )
            
            submitted = st.form_submit_button("Submit", type="primary")
            
            if submitted:
                on_submit(form_data)
                st.rerun()
