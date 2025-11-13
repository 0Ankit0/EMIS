"""
Student Library Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from components.ui_components import render_data_table


def show():
    """Display student library page"""
    st.title("📚 Library")
    st.markdown("### Search books and manage your library account")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Search Books", "📖 My Books", "💰 Fines"])
    
    with tab1:
        show_search_books()
    
    with tab2:
        show_my_books()
    
    with tab3:
        show_fines()


def show_search_books():
    """Show book search interface"""
    st.subheader("Search Books")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search by title, author, or ISBN", placeholder="Enter search term...")
    
    with col2:
        category = st.selectbox("Category", ["All", "Computer Science", "Mathematics", "Physics", "Chemistry", "Literature"])
    
    if search_query or category != "All":
        try:
            params = {}
            if search_query:
                params["query"] = search_query
            if category != "All":
                params["category"] = category
            
            response = api_client.get("/api/library/books/search", params=params)
            books = response.get("items", [])
            
            if books:
                st.write(f"Found {len(books)} books")
                
                for book in books:
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"### 📖 {book.get('title', 'Book')}")
                            st.write(f"**Author:** {book.get('author', 'N/A')}")
                            st.write(f"**ISBN:** {book.get('isbn', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Category:** {book.get('category', 'N/A')}")
                            st.write(f"**Publisher:** {book.get('publisher', 'N/A')}")
                        
                        with col3:
                            available = book.get('available_copies', 0)
                            if available > 0:
                                st.success(f"✅ {available} copies available")
                                if st.button("Reserve Book", key=f"reserve_{book.get('id')}"):
                                    reserve_book(book.get('id'))
                            else:
                                st.error("❌ Not available")
                        
                        st.divider()
            else:
                show_info("No books found matching your search")
        
        except Exception as e:
            show_error(f"Error searching books: {str(e)}")


def show_my_books():
    """Show issued books"""
    st.subheader("My Issued Books")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/library/issued")
        
        books = response.get("items", [])
        
        if books:
            for book in books:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**📖 {book.get('title', 'Book')}**")
                        st.write(f"Author: {book.get('author', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Issue Date:** {book.get('issue_date', 'N/A')}")
                        st.write(f"**Due Date:** {book.get('due_date', 'N/A')}")
                    
                    with col3:
                        # Check if overdue
                        is_overdue = book.get('is_overdue', False)
                        if is_overdue:
                            st.error(f"⚠️ Overdue!")
                            fine = book.get('fine_amount', 0)
                            if fine > 0:
                                st.write(f"Fine: ₹{fine}")
                        else:
                            days_left = book.get('days_remaining', 0)
                            if days_left <= 3:
                                st.warning(f"⏰ {days_left} days left")
                            else:
                                st.info(f"📅 {days_left} days left")
                        
                        if st.button("Renew", key=f"renew_{book.get('id')}"):
                            renew_book(book.get('id'))
                    
                    st.divider()
        else:
            show_info("You don't have any issued books")
    
    except Exception as e:
        show_error(f"Error loading issued books: {str(e)}")


def show_fines():
    """Show library fines"""
    st.subheader("Library Fines")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/library/fines")
        
        total_fine = response.get("total_fine", 0)
        
        if total_fine > 0:
            st.error(f"💰 Total Outstanding Fine: ₹{total_fine}")
            
            fines = response.get("items", [])
            
            if fines:
                df = pd.DataFrame(fines)
                display_columns = ["book_title", "due_date", "return_date", "days_overdue", "fine_amount", "status"]
                available_columns = [col for col in display_columns if col in df.columns]
                
                render_data_table(df[available_columns], "Fine Details")
                
                st.divider()
                
                if st.button("💳 Pay All Fines", type="primary"):
                    pay_fines(total_fine)
        else:
            st.success("✅ No outstanding fines!")
    
    except Exception as e:
        show_error(f"Error loading fines: {str(e)}")


def reserve_book(book_id):
    """Reserve a book"""
    try:
        student_id = st.session_state.user.get("id")
        data = {
            "student_id": student_id,
            "book_id": book_id
        }
        response = api_client.post("/api/library/reserve", data)
        show_success("Book reserved successfully! Please collect within 24 hours.")
    except Exception as e:
        show_error(f"Error reserving book: {str(e)}")


def renew_book(issue_id):
    """Renew an issued book"""
    try:
        response = api_client.post(f"/api/library/issues/{issue_id}/renew")
        show_success("Book renewed successfully!")
        st.rerun()
    except Exception as e:
        show_error(f"Error renewing book: {str(e)}")


def pay_fines(amount):
    """Pay library fines"""
    try:
        student_id = st.session_state.user.get("id")
        data = {
            "student_id": student_id,
            "amount": amount
        }
        response = api_client.post("/api/library/fines/pay", data)
        show_success(f"Fine of ₹{amount} paid successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error paying fine: {str(e)}")
