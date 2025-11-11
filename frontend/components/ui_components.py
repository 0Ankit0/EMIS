"""
Reusable UI Components
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import pandas as pd


def render_card(title: str, value: Any, icon: str = "📊", color: str = "#0066cc"):
    """Render a metric card"""
    st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
            border-left: 4px solid {color};
            margin: 10px 0;
        ">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2em; margin-right: 15px;">{icon}</span>
                <div>
                    <p style="margin: 0; color: #666; font-size: 0.9em;">{title}</p>
                    <h2 style="margin: 5px 0; color: {color};">{value}</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_stats_cards(stats: List[Dict[str, Any]]):
    """Render multiple stat cards in columns"""
    cols = st.columns(len(stats))
    
    for col, stat in zip(cols, stats):
        with col:
            render_card(
                stat.get("title", ""),
                stat.get("value", 0),
                stat.get("icon", "📊"),
                stat.get("color", "#0066cc")
            )


def render_data_table(
    data: pd.DataFrame,
    title: Optional[str] = None,
    searchable: bool = True,
    downloadable: bool = True
):
    """Render a data table with search and download options"""
    if title:
        st.subheader(title)
    
    # Search functionality
    if searchable and not data.empty:
        search = st.text_input("🔍 Search", key=f"search_{title}")
        if search:
            mask = data.astype(str).apply(
                lambda x: x.str.contains(search, case=False, na=False)
            ).any(axis=1)
            data = data[mask]
    
    # Display table
    st.dataframe(data, use_container_width=True)
    
    # Download button
    if downloadable and not data.empty:
        csv = data.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            f"{title or 'data'}.csv",
            "text/csv"
        )


def render_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None
):
    """Render a bar chart"""
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_line_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: Optional[str] = None
):
    """Render a line chart"""
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        markers=True
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_pie_chart(
    data: pd.DataFrame,
    names: str,
    values: str,
    title: str
):
    """Render a pie chart"""
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        hole=0.4
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_gauge_chart(value: float, title: str, max_value: float = 100):
    """Render a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        delta={'reference': max_value * 0.8},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "#0066cc"},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def render_progress_bar(value: float, label: str, max_value: float = 100):
    """Render a progress bar"""
    percentage = (value / max_value) * 100
    st.write(label)
    st.progress(percentage / 100)
    st.caption(f"{value:.1f} / {max_value:.1f} ({percentage:.1f}%)")


def render_sidebar_menu(menu_items: List[Dict[str, Any]]) -> str:
    """Render sidebar navigation menu"""
    with st.sidebar:
        st.title("📚 EMIS")
        st.divider()
        
        selected = None
        for item in menu_items:
            if st.button(
                f"{item['icon']} {item['label']}",
                key=item['key'],
                use_container_width=True
            ):
                selected = item['key']
        
        return selected


def render_confirmation_dialog(message: str, key: str = "confirm") -> bool:
    """Render a confirmation dialog"""
    with st.expander("⚠️ Confirm Action", expanded=False):
        st.warning(message)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", key=f"{key}_yes"):
                return True
        with col2:
            if st.button("❌ Cancel", key=f"{key}_no"):
                return False
    return False


def render_form_field(
    label: str,
    field_type: str = "text",
    required: bool = False,
    **kwargs
):
    """Render a form field"""
    label_text = f"{label} {'*' if required else ''}"
    
    if field_type == "text":
        return st.text_input(label_text, **kwargs)
    elif field_type == "number":
        return st.number_input(label_text, **kwargs)
    elif field_type == "date":
        return st.date_input(label_text, **kwargs)
    elif field_type == "select":
        return st.selectbox(label_text, **kwargs)
    elif field_type == "multiselect":
        return st.multiselect(label_text, **kwargs)
    elif field_type == "textarea":
        return st.text_area(label_text, **kwargs)
    elif field_type == "checkbox":
        return st.checkbox(label_text, **kwargs)
    elif field_type == "file":
        return st.file_uploader(label_text, **kwargs)
    else:
        return st.text_input(label_text, **kwargs)
