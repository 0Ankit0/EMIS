"""
Notification Utilities
"""
import streamlit as st
from typing import Optional
from datetime import datetime


class NotificationManager:
    """Manage notifications in the application"""
    
    @staticmethod
    def show_success(message: str, icon: str = "✅"):
        """Show success notification"""
        st.success(f"{icon} {message}")
    
    @staticmethod
    def show_error(message: str, icon: str = "❌"):
        """Show error notification"""
        st.error(f"{icon} {message}")
    
    @staticmethod
    def show_warning(message: str, icon: str = "⚠️"):
        """Show warning notification"""
        st.warning(f"{icon} {message}")
    
    @staticmethod
    def show_info(message: str, icon: str = "ℹ️"):
        """Show info notification"""
        st.info(f"{icon} {message}")
    
    @staticmethod
    def show_toast(message: str, duration: int = 3):
        """Show toast notification"""
        st.toast(message, icon="🔔")
    
    @staticmethod
    def show_notification_card(title: str, message: str, notification_type: str = "info"):
        """Show notification card"""
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        icon = icons.get(notification_type, "ℹ️")
        
        with st.container():
            st.markdown(f"""
            <div style="
                padding: 1rem;
                border-left: 4px solid {'#28a745' if notification_type == 'success' else '#dc3545' if notification_type == 'error' else '#ffc107' if notification_type == 'warning' else '#17a2b8'};
                background-color: #f8f9fa;
                margin: 0.5rem 0;
            ">
                <strong>{icon} {title}</strong><br/>
                {message}
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def add_notification_to_queue(user_id: int, title: str, message: str, notification_type: str = "info"):
        """Add notification to user's queue (stored in session state)"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        notification = {
            "id": len(st.session_state.notifications) + 1,
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        st.session_state.notifications.append(notification)
    
    @staticmethod
    def get_unread_notifications(user_id: int) -> list:
        """Get unread notifications for user"""
        if 'notifications' not in st.session_state:
            return []
        
        return [n for n in st.session_state.notifications 
                if n['user_id'] == user_id and not n['read']]
    
    @staticmethod
    def mark_as_read(notification_id: int):
        """Mark notification as read"""
        if 'notifications' in st.session_state:
            for notification in st.session_state.notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    break
    
    @staticmethod
    def show_notification_bell():
        """Show notification bell with unread count"""
        user_id = st.session_state.get('user', {}).get('id')
        if user_id:
            unread = NotificationManager.get_unread_notifications(user_id)
            count = len(unread)
            
            if count > 0:
                st.sidebar.markdown(f"""
                <div style="
                    background-color: #dc3545;
                    color: white;
                    border-radius: 50%;
                    width: 25px;
                    height: 25px;
                    text-align: center;
                    line-height: 25px;
                    font-size: 12px;
                    position: absolute;
                    top: 10px;
                    right: 10px;
                ">
                    {count}
                </div>
                """, unsafe_allow_html=True)


# Singleton instance
notification_manager = NotificationManager()
