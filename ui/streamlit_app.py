# ui/streamlit_app.py - Main Streamlit Application
import streamlit as st
import pandas as pd
import asyncio
from workflows.monitoring_workflow import MonitoringWorkflow
from tools.human_approval_tool import HumanApprovalTool
from config.database import test_connection

class AgenticMonitoringUI:
    def __init__(self):
        st.set_page_config(
            page_title="AGNO Agentic Pipeline Monitor",
            page_icon="🤖",
            layout="wide"
        )
        
        self.approval_tool = HumanApprovalTool()
    
    def main_dashboard(self):
        st.title("🤖 AGNO Agentic Pipeline Monitor")
        st.markdown("**AI-Powered Pipeline Monitoring with Human-in-the-Loop**")
        
        # Sidebar
        with st.sidebar:
            st.header("🔧 Configuration")
            
            # Database status
            db_status = test_connection()
            st.metric("MySQL Status", "🟢 Connected" if db_status else "🔴 Disconnected")
            
            # Upload data
            uploaded_file = st.file_uploader("Upload Pipeline Data", type=['csv', 'xlsx'])
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["📊 Monitor", "✋ Approvals", "📈 History"])
        
        with tab1:
            self.monitoring_tab(uploaded_file)
        
        with tab2:
            self.approval_tab()
        
        with tab3:
            self.history_tab()
    
    def approval_tab(self):
        """Human approval interface"""
        st.subheader("👤 Pending Approvals")
        
        pending_approvals = self.approval_tool.get_pending_approvals()
        
        if not pending_approvals:
            st.success("No pending approvals")
            return
        
        for approval in pending_approvals:
            with st.expander(f"📋 {approval.action_type} (Risk: {approval.risk_level})"):
                st.write(f"**Description:** {approval.description}")
                st.write(f"**Created:** {approval.created_at}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{approval.id}"):
                        reason = st.text_input("Approval reason:", key=f"approve_reason_{approval.id}")
                        self.approval_tool.update_approval_decision(approval.id, "approve", reason)
                        st.success("Approved!")
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Deny", key=f"deny_{approval.id}"):
                        reason = st.text_input("Denial reason:", key=f"deny_reason_{approval.id}")
                        self.approval_tool.update_approval_decision(approval.id, "deny", reason)
                        st.error("Denied!")
                        st.rerun()

if __name__ == "__main__":
    ui = AgenticMonitoringUI()
    ui.main_dashboard()