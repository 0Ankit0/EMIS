"""
Student Fees and Payments Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info, format_currency
from components.ui_components import render_data_table


def show():
    """Display student fees and payments page"""
    st.title("💰 Fees & Payments")
    st.markdown("### Manage your fees and payment history")
    
    tab1, tab2, tab3 = st.tabs(["💳 Pay Fees", "📋 Fee Structure", "📊 Payment History"])
    
    with tab1:
        show_pay_fees()
    
    with tab2:
        show_fee_structure()
    
    with tab3:
        show_payment_history()


def show_pay_fees():
    """Show fee payment interface"""
    st.subheader("Pay Fees")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/fees/pending")
        
        total_pending = response.get("total_pending", 0)
        
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Fees", format_currency(response.get("total_fees", 0)))
        
        with col2:
            st.metric("Paid", format_currency(response.get("total_paid", 0)))
        
        with col3:
            st.metric("Pending", format_currency(total_pending), delta=f"-{total_pending}")
        
        if total_pending > 0:
            st.divider()
            st.subheader("💳 Make Payment")
            
            # Fee breakup
            st.write("**Fee Breakup:**")
            fee_items = response.get("fee_items", [])
            
            for item in fee_items:
                if item.get("status") == "pending":
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"• {item.get('description', 'Fee')}")
                    with col2:
                        st.write(format_currency(item.get('amount', 0)))
            
            st.divider()
            
            # Payment options
            st.write("**Select Payment Method:**")
            payment_method = st.radio(
                "Payment Method",
                ["Online Payment (Credit/Debit Card)", "Net Banking", "UPI", "Pay at Counter"],
                label_visibility="collapsed"
            )
            
            amount_to_pay = st.number_input(
                "Amount to Pay",
                min_value=0.0,
                max_value=float(total_pending),
                value=float(total_pending),
                step=100.0
            )
            
            if st.button("💳 Proceed to Payment", type="primary"):
                process_payment(amount_to_pay, payment_method)
        else:
            st.success("✅ All fees paid! No pending payments.")
    
    except Exception as e:
        show_error(f"Error loading fee information: {str(e)}")
        show_demo_fees()


def show_fee_structure():
    """Show fee structure"""
    st.subheader("Fee Structure")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/fees/structure")
        
        fee_structure = response.get("items", [])
        
        if fee_structure:
            total = 0
            for category in fee_structure:
                with st.expander(f"📋 {category.get('category', 'Category')}", expanded=True):
                    items = category.get('items', [])
                    category_total = 0
                    
                    for item in items:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(item.get('description', ''))
                        
                        with col2:
                            amount = item.get('amount', 0)
                            st.write(format_currency(amount))
                            category_total += amount
                        
                        with col3:
                            status = item.get('status', 'pending')
                            if status == 'paid':
                                st.success("✅ Paid")
                            else:
                                st.warning("⏳ Pending")
                    
                    st.divider()
                    st.write(f"**{category.get('category')} Total:** {format_currency(category_total)}")
                    total += category_total
            
            st.divider()
            st.markdown(f"### **Grand Total:** {format_currency(total)}")
        else:
            show_info("Fee structure not available")
    
    except Exception as e:
        show_error(f"Error loading fee structure: {str(e)}")


def show_payment_history():
    """Show payment history"""
    st.subheader("Payment History")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/payments/history")
        
        payments = response.get("items", [])
        
        if payments:
            df = pd.DataFrame(payments)
            display_columns = ["payment_date", "amount", "payment_method", "receipt_no", "status"]
            available_columns = [col for col in display_columns if col in df.columns]
            
            render_data_table(df[available_columns], "Payment History")
            
            # Download receipt option
            st.divider()
            receipt_no = st.selectbox("Select Receipt to Download", df["receipt_no"].tolist() if "receipt_no" in df.columns else [])
            
            if st.button("📥 Download Receipt"):
                download_receipt(receipt_no)
        else:
            show_info("No payment history available")
    
    except Exception as e:
        show_error(f"Error loading payment history: {str(e)}")


def process_payment(amount, method):
    """Process fee payment"""
    try:
        student_id = st.session_state.user.get("id")
        data = {
            "student_id": student_id,
            "amount": amount,
            "payment_method": method
        }
        response = api_client.post("/api/students/payments", data)
        show_success(f"Payment of {format_currency(amount)} processed successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error processing payment: {str(e)}")


def download_receipt(receipt_no):
    """Download payment receipt"""
    try:
        response = api_client.get(f"/api/students/receipts/{receipt_no}", stream=True)
        st.success("Receipt download started!")
    except Exception as e:
        show_error(f"Error downloading receipt: {str(e)}")


def show_demo_fees():
    """Show demo fee data"""
    st.info("Showing demo data...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Fees", "₹75,000")
    with col2:
        st.metric("Paid", "₹50,000")
    with col3:
        st.metric("Pending", "₹25,000", delta="-25000")
    
    st.divider()
    st.subheader("💳 Make Payment")
    
    st.write("**Fee Breakup:**")
    st.write("• Tuition Fee: ₹15,000")
    st.write("• Library Fee: ₹5,000")
    st.write("• Lab Fee: ₹5,000")
