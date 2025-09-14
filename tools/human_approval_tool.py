# tools/human_approval_tool.py - SQL Server Compatible
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.database import SessionLocal, Base, engine

class ApprovalRequest(Base):
    """SQL Server compatible approval request model"""
    __tablename__ = "approval_requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    action_type = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    risk_level = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    decision = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

class HumanApprovalTool:
    def __init__(self):
        self.name = "human_approval"
        self.description = "Request human approval for pipeline actions"
        
        # Ensure table exists
        self._ensure_table()
    
    def _ensure_table(self):
        """Ensure approval_requests table exists"""
        try:
            Base.metadata.create_all(bind=engine, tables=[ApprovalRequest.__table__])
        except Exception as e:
            print(f"⚠️ Could not ensure table exists: {e}")
    
    def request_approval_console(self, action_type: str, description: str, risk_level: str = "medium"):
        """Console-based approval for command line usage"""
        print("\n" + "="*60)
        print("🚨 HUMAN APPROVAL REQUIRED")
        print("="*60)
        print(f"📋 Action: {action_type}")
        print(f"📝 Description: {description}")
        print(f"⚠️ Risk Level: {risk_level.upper()}")
        print("="*60)
        
        while True:
            decision = input("\nDecision (approve/deny/modify): ").lower().strip()
            
            if decision in ['approve', 'approved', 'a', 'yes', 'y']:
                print("✅ APPROVED - Proceeding with action")
                self._log_decision_to_db(action_type, description, risk_level, "approved")
                return "approved"
            elif decision in ['deny', 'denied', 'd', 'no', 'n']:
                reason = input("Denial reason: ")
                print(f"❌ DENIED - Reason: {reason}")
                decision_text = f"denied: {reason}"
                self._log_decision_to_db(action_type, description, risk_level, decision_text)
                return decision_text
            elif decision in ['modify', 'modified', 'm']:
                modifications = input("Requested modifications: ")
                print(f"🔄 MODIFY - Changes: {modifications}")
                decision_text = f"modified: {modifications}"
                self._log_decision_to_db(action_type, description, risk_level, decision_text)
                return decision_text
            else:
                print("Please enter 'approve', 'deny', or 'modify'")
    
    def _log_decision_to_db(self, action_type: str, description: str, risk_level: str, decision: str):
        """Log decision to SQL Server database"""
        try:
            db = SessionLocal()
            approval_request = ApprovalRequest(
                action_type=action_type,
                description=description,
                risk_level=risk_level,
                status="approved" if decision.startswith("approved") else "denied",
                decision=decision,
                decided_at=datetime.utcnow()
            )
            db.add(approval_request)
            db.commit()
            print(f"📝 Decision logged to database (ID: {approval_request.id})")
        except Exception as e:
            print(f"⚠️ Could not log to database: {e}")
        finally:
            db.close()
    
    def request_approval_db(self, action_type: str, description: str, risk_level: str = "medium"):
        """Database-based approval for UI usage"""
        try:
            db = SessionLocal()
            approval_request = ApprovalRequest(
                action_type=action_type,
                description=description,
                risk_level=risk_level,
                status="pending"
            )
            db.add(approval_request)
            db.commit()
            
            print(f"\n🚨 APPROVAL REQUEST CREATED (ID: {approval_request.id})")
            print(f"📋 Action: {action_type}")
            print(f"📝 Description: {description}")
            print(f"⚠️ Risk Level: {risk_level}")
            print("👤 Check UI for approval...")
            
            return approval_request.id
        except Exception as e:
            print(f"❌ Failed to create approval request: {e}")
            return None
        finally:
            db.close()
    
    def get_pending_approvals(self):
        """Get all pending approval requests"""
        try:
            db = SessionLocal()
            return db.query(ApprovalRequest).filter(ApprovalRequest.status == "pending").all()
        except Exception as e:
            print(f"❌ Failed to get pending approvals: {e}")
            return []
        finally:
            db.close()
    
    def update_approval_decision(self, request_id: int, decision: str, reason: str = ""):
        """Update approval decision in database"""
        try:
            db = SessionLocal()
            request = db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
            if request:
                request.status = "approved" if decision == "approve" else "denied"
                request.decision = f"{decision}: {reason}" if reason else decision
                request.decided_at = datetime.utcnow()
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to update approval: {e}")
            return False
        finally:
            db.close()

if __name__ == "__main__":
    # Test the tool
    print("🧪 Testing Human Approval Tool with SQL Server...")
    tool = HumanApprovalTool()
    
    # Test console approval
    print("\n1. Testing console approval:")
    decision = tool.request_approval_console("Test Action", "Testing approval system", "low")
    print(f"Decision received: {decision}")
    
    # Test database functionality
    print("\n2. Testing database functionality:")
    pending = tool.get_pending_approvals()
    print(f"Pending approvals: {len(pending)}")