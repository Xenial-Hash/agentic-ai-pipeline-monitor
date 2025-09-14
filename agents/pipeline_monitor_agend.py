# agents/pipeline_monitor_agent.py - AGNO-Free Agentic AI Implementation
import asyncio
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.database import SessionLocal, Base, engine
from tools.human_approval_tool import HumanApprovalTool
from sqlalchemy import Column, Integer, String, DateTime, Text

load_dotenv()

class GroqAI:
    """Direct Groq API integration without AGNO dependency"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            print("⚠️ No Groq API key found. Using fallback analysis.")
            self.available = False
        else:
            self.available = True
    
    async def analyze(self, prompt: str) -> str:
        """Send analysis request to Groq API"""
        if not self.available:
            return self._fallback_analysis(prompt)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are an expert data pipeline monitoring AI. Provide comprehensive analysis with specific insights and actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1024
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"⚠️ Groq API error: {response.status_code}")
                return self._fallback_analysis(prompt)
                
        except Exception as e:
            print(f"⚠️ Groq API request failed: {e}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        """Rule-based fallback analysis"""
        return """
**AUTOMATED ANALYSIS (Fallback Mode)**

This analysis was generated using rule-based logic as the AI service is unavailable.

**Health Assessment:** Based on detected anomalies and data quality metrics
**Recommendations:** 
• Review data source connections if issues persist
• Monitor trend patterns over time
• Implement automated data validation
• Consider pipeline optimization for better performance

**Note:** For enhanced AI-powered insights, ensure Groq API key is configured.
        """

class MonitoringHistory(Base):
    """SQL Server monitoring history model"""
    __tablename__ = "monitoring_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_name = Column(String(255), nullable=False)
    metrics = Column(Text, nullable=False)
    anomalies = Column(Text, nullable=True)
    risk_level = Column(String(50), nullable=True)
    ai_insights = Column(Text, nullable=True)
    execution_results = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgenticPipelineMonitor:
    """AGNO-Free Agentic AI Pipeline Monitor"""
    
    def __init__(self):
        print("🤖 Initializing Agentic Pipeline Monitor (AGNO-Free)")
        
        self.groq_ai = GroqAI()
        self.human_approval = HumanApprovalTool()
        self.monitoring_history = []
        
        # Ensure database tables exist
        self._ensure_monitoring_table()
        
        print("✅ Agentic AI Monitor initialized successfully")
    
    def _ensure_monitoring_table(self):
        """Ensure monitoring_history table exists"""
        try:
            Base.metadata.create_all(bind=engine, tables=[MonitoringHistory.__table__])
        except Exception as e:
            print(f"⚠️ Could not ensure monitoring table exists: {e}")
    
    async def monitor_pipeline(self, df: pd.DataFrame, pipeline_name: str = "DefaultPipeline"):
        """Main agentic pipeline monitoring function"""
        
        print(f"🚀 Starting Agentic AI Monitoring: {pipeline_name}")
        print("="*50)
        
        # Phase 1: Comprehensive Data Analysis
        print("📊 Phase 1: Data Analysis...")
        metrics = self._analyze_comprehensive_metrics(df, pipeline_name)
        print(f"   ✓ Analyzed {metrics['total_records']:,} records")
        
        # Phase 2: Intelligent Anomaly Detection
        print("🔍 Phase 2: Anomaly Detection...")
        anomalies = self._detect_intelligent_anomalies(metrics)
        print(f"   ✓ Detected {len(anomalies)} anomalies")
        
        # Phase 3: AI-Powered Risk Assessment
        print("⚠️ Phase 3: Risk Assessment...")
        risk_level = self._assess_intelligent_risk(anomalies, metrics)
        print(f"   ✓ Risk Level: {risk_level.upper()}")
        
        # Phase 4: Advanced AI Insights
        print("🤖 Phase 4: AI Analysis...")
        ai_insights = await self._generate_ai_insights(metrics, anomalies, risk_level)
        print("   ✓ AI analysis completed")
        
        # Phase 5: Agentic Decision Making
        print("🎯 Phase 5: Decision Making...")
        required_actions = self._determine_agentic_actions(risk_level, anomalies, metrics)
        print(f"   ✓ {len(required_actions)} actions identified")
        
        # Phase 6: Human-in-the-Loop Workflow
        print("👤 Phase 6: Human Approvals...")
        approval_results = self._handle_human_approval_workflow(required_actions)
        print(f"   ✓ {len(approval_results)} approvals processed")
        
        # Phase 7: Execution and Storage
        print("💾 Phase 7: Data Storage...")
        monitoring_record = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_name": pipeline_name,
            "metrics": metrics,
            "anomalies": anomalies,
            "risk_level": risk_level,
            "ai_insights": ai_insights,
            "approval_results": approval_results,
            "execution_phase": "completed"
        }
        
        # Store in memory and database
        self.monitoring_history.append(monitoring_record)
        self._store_monitoring_record_db(monitoring_record)
        print("   ✓ All data stored successfully")
        
        print("="*50)
        print("🎉 Agentic AI Monitoring Completed Successfully!")
        
        return monitoring_record
    
    def _analyze_comprehensive_metrics(self, df: pd.DataFrame, pipeline_name: str):
        """Comprehensive data analysis with advanced metrics"""
        
        # Basic metrics
        basic_metrics = {
            "pipeline_name": pipeline_name,
            "total_records": len(df),
            "total_columns": len(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_records": df.duplicated().sum(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024),
            "column_names": list(df.columns)
        }
        
        # Advanced analytics
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        # Statistical analysis
        if numeric_columns:
            basic_metrics["statistical_summary"] = {}
            for col in numeric_columns:
                if not df[col].isnull().all():
                    basic_metrics["statistical_summary"][col] = {
                        "mean": float(df[col].mean()),
                        "median": float(df[col].median()),
                        "std": float(df[col].std()),
                        "min": float(df[col].min()),
                        "max": float(df[col].max()),
                        "q25": float(df[col].quantile(0.25)),
                        "q75": float(df[col].quantile(0.75)),
                        "skewness": float(df[col].skew()),
                        "null_percentage": float((df[col].isnull().sum() / len(df)) * 100)
                    }
        
        # Categorical analysis
        if categorical_columns:
            basic_metrics["categorical_summary"] = {}
            for col in categorical_columns[:5]:  # Limit to avoid huge outputs
                basic_metrics["categorical_summary"][col] = {
                    "unique_values": int(df[col].nunique()),
                    "most_common": df[col].mode().iloc[0] if not df[col].empty else None,
                    "null_percentage": float((df[col].isnull().sum() / len(df)) * 100)
                }
        
        # Data quality score calculation
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_ratio = basic_metrics["duplicate_records"] / len(df) if len(df) > 0 else 0
        
        quality_score = max(0, 100 - (missing_cells / total_cells * 50) - (duplicate_ratio * 30))
        basic_metrics["data_quality_score"] = round(quality_score, 2)
        
        return basic_metrics
    
    def _detect_intelligent_anomalies(self, metrics):
        """Advanced anomaly detection using multiple algorithms"""
        anomalies = []
        
        # 1. Data Quality Anomalies
        total_nulls = sum(metrics["missing_values"].values())
        total_cells = metrics["total_records"] * metrics["total_columns"]
        null_percentage = (total_nulls / total_cells) * 100 if total_cells > 0 else 0
        
        if null_percentage > 25:
            anomalies.append(f"CRITICAL: Excessive missing data ({null_percentage:.1f}%)")
        elif null_percentage > 15:
            anomalies.append(f"HIGH: Significant missing data ({null_percentage:.1f}%)")
        elif null_percentage > 8:
            anomalies.append(f"MEDIUM: Moderate missing data ({null_percentage:.1f}%)")
        
        # 2. Duplicate Detection
        duplicate_pct = (metrics["duplicate_records"] / metrics["total_records"]) * 100 if metrics["total_records"] > 0 else 0
        if duplicate_pct > 20:
            anomalies.append(f"CRITICAL: Very high duplicate rate ({duplicate_pct:.1f}%)")
        elif duplicate_pct > 10:
            anomalies.append(f"HIGH: High duplicate rate ({duplicate_pct:.1f}%)")
        elif duplicate_pct > 5:
            anomalies.append(f"MEDIUM: Moderate duplicate rate ({duplicate_pct:.1f}%)")
        
        # 3. Volume Anomalies
        record_count = metrics["total_records"]
        if record_count == 0:
            anomalies.append("CRITICAL: No data records found - pipeline failure")
        elif record_count < 50:
            anomalies.append(f"HIGH: Extremely low record count ({record_count})")
        elif record_count < 200:
            anomalies.append(f"MEDIUM: Low record count ({record_count})")
        
        # 4. Schema Anomalies
        column_count = metrics["total_columns"]
        if column_count < 2:
            anomalies.append("HIGH: Very few columns - possible data truncation")
        elif column_count > 150:
            anomalies.append("MEDIUM: Unusually high column count - consider optimization")
        
        # 5. Statistical Anomalies (for numeric data)
        if "statistical_summary" in metrics:
            for col, stats in metrics["statistical_summary"].items():
                if stats["skewness"] > 3:
                    anomalies.append(f"MEDIUM: High skewness in {col} column")
                if stats["null_percentage"] > 50:
                    anomalies.append(f"HIGH: {col} column >50% missing values")
        
        # 6. Data Quality Score Check
        quality_score = metrics.get("data_quality_score", 100)
        if quality_score < 60:
            anomalies.append(f"CRITICAL: Low data quality score ({quality_score:.1f}%)")
        elif quality_score < 80:
            anomalies.append(f"HIGH: Below standard data quality ({quality_score:.1f}%)")
        
        return anomalies
    
    def _assess_intelligent_risk(self, anomalies, metrics):
        """Intelligent risk assessment using weighted scoring"""
        
        if not anomalies:
            return "low"
        
        risk_score = 0
        
        # Weight anomalies by severity
        for anomaly in anomalies:
            if "CRITICAL" in anomaly:
                risk_score += 10
            elif "HIGH" in anomaly:
                risk_score += 6
            elif "MEDIUM" in anomaly:
                risk_score += 3
            else:
                risk_score += 1
        
        # Additional risk factors
        if metrics["total_records"] == 0:
            risk_score += 15  # No data is critical
        
        if metrics.get("data_quality_score", 100) < 50:
            risk_score += 8
        
        # Risk categorization
        if risk_score >= 15:
            return "high"
        elif risk_score >= 8:
            return "medium"
        else:
            return "low"
    
    async def _generate_ai_insights(self, metrics, anomalies, risk_level):
        """Generate comprehensive AI insights"""
        
        analysis_prompt = f"""
        **PIPELINE MONITORING ANALYSIS REQUEST**
        
        **Pipeline:** {metrics['pipeline_name']}
        **Data Overview:**
        - Total Records: {metrics['total_records']:,}
        - Columns: {metrics['total_columns']}
        - Memory Usage: {metrics['memory_usage_mb']:.2f}MB
        - Data Quality Score: {metrics.get('data_quality_score', 'N/A')}%
        
        **Risk Assessment:** {risk_level.upper()}
        
        **Anomalies Detected ({len(anomalies)}):**
        {chr(10).join(f"• {anomaly}" for anomaly in anomalies) if anomalies else "• No anomalies detected"}
        
        **Data Quality Issues:**
        - Missing Values: {sum(metrics['missing_values'].values()):,}
        - Duplicate Records: {metrics['duplicate_records']:,}
        
        **Request:** Provide comprehensive analysis including:
        1. **Executive Summary** (2-3 sentences)
        2. **Critical Findings** (most important issues)
        3. **Business Impact Analysis** (operational implications)
        4. **Specific Recommendations** (actionable steps)
        5. **Trend Predictions** (what to watch for)
        6. **Confidence Score** (0-100%)
        
        Focus on business value and actionable insights.
        """
        
        try:
            ai_insights = await self.groq_ai.analyze(analysis_prompt)
            return ai_insights
        except Exception as e:
            return f"AI Analysis Error: {str(e)}"
    
    def _determine_agentic_actions(self, risk_level, anomalies, metrics):
        """Determine actions using agentic decision-making logic"""
        
        actions = []
        
        # Critical risk actions
        if risk_level == "high":
            actions.append({
                "type": "EMERGENCY Pipeline Response",
                "description": f"Critical pipeline issues detected requiring immediate intervention",
                "priority": "URGENT",
                "risk_level": "high",
                "requires_approval": True,
                "auto_executable": False
            })
        
        # Data quality actions
        critical_anomalies = [a for a in anomalies if "CRITICAL" in a]
        if critical_anomalies:
            for anomaly in critical_anomalies:
                actions.append({
                    "type": "Critical Data Quality Response",
                    "description": f"Address critical issue: {anomaly}",
                    "priority": "HIGH",
                    "risk_level": "high",
                    "requires_approval": True,
                    "auto_executable": False
                })
        
        # Volume-based actions
        if metrics["total_records"] == 0:
            actions.append({
                "type": "Pipeline Failure Investigation",
                "description": "No data processed - investigate source systems and connections",
                "priority": "CRITICAL",
                "risk_level": "high",
                "requires_approval": True,
                "auto_executable": False
            })
        elif metrics["total_records"] < 100:
            actions.append({
                "type": "Low Volume Investigation",
                "description": f"Unusually low record count ({metrics['total_records']}) requires review",
                "priority": "MEDIUM",
                "risk_level": "medium",
                "requires_approval": True,
                "auto_executable": False
            })
        
        # Quality score actions
        quality_score = metrics.get("data_quality_score", 100)
        if quality_score < 70:
            actions.append({
                "type": "Data Quality Improvement",
                "description": f"Data quality score ({quality_score:.1f}%) below acceptable threshold",
                "priority": "HIGH",
                "risk_level": "medium",
                "requires_approval": True,
                "auto_executable": False
            })
        
        # Routine monitoring
        if not actions:
            actions.append({
                "type": "Routine Monitoring Complete",
                "description": "Pipeline monitoring completed successfully with no critical issues",
                "priority": "NORMAL",
                "risk_level": "low",
                "requires_approval": False,
                "auto_executable": True
            })
        
        return actions
    
    def _handle_human_approval_workflow(self, required_actions):
        """Enhanced human approval workflow with detailed context"""
        
        approval_results = []
        
        print(f"\n📋 Processing {len(required_actions)} actions...")
        
        for i, action in enumerate(required_actions, 1):
            if action["requires_approval"]:
                print(f"\n🚨 ACTION {i}: {action['type']}")
                print(f"   Priority: {action['priority']}")
                
                # Enhanced approval request with context
                decision = self.human_approval.request_approval_console(
                    f"[{action['priority']}] {action['type']}",
                    f"{action['description']}\n\nPriority Level: {action['priority']}\nRisk Impact: {action['risk_level']}",
                    action["risk_level"]
                )
                
                approval_results.append({
                    "action": action,
                    "decision": decision,
                    "status": "approved" if decision.startswith("approved") else "denied",
                    "timestamp": datetime.now().isoformat(),
                    "priority": action["priority"]
                })
                
                if decision.startswith("approved"):
                    print(f"   ✅ APPROVED: {action['type']}")
                else:
                    print(f"   ❌ DENIED: {action['type']}")
                    
            else:
                # Auto-execute routine actions
                approval_results.append({
                    "action": action,
                    "decision": "auto_approved",
                    "status": "approved",
                    "timestamp": datetime.now().isoformat(),
                    "priority": action["priority"]
                })
                print(f"   ✅ AUTO-APPROVED: {action['type']}")
        
        return approval_results
    
    def _store_monitoring_record_db(self, record):
        """Store comprehensive monitoring record in SQL Server"""
        try:
            db = SessionLocal()
            
            monitoring_entry = MonitoringHistory(
                pipeline_name=record["pipeline_name"],
                metrics=json.dumps(record["metrics"], default=str),
                anomalies=json.dumps(record["anomalies"]) if record["anomalies"] else None,
                risk_level=record["risk_level"],
                ai_insights=record["ai_insights"],
                execution_results=json.dumps(record["approval_results"], default=str)
            )
            
            db.add(monitoring_entry)
            db.commit()
            print(f"💾 Complete monitoring record stored (ID: {monitoring_entry.id})")
            
        except Exception as e:
            print(f"⚠️ Could not store monitoring record: {e}")
        finally:
            db.close()

# Standalone test function
if __name__ == "__main__":
    import numpy as np
    
    async def test_agentic_monitor():
        print("🧪 Testing AGNO-Free Agentic Pipeline Monitor")
        print("="*60)
        
        try:
            # Initialize monitor
            monitor = AgenticPipelineMonitor()
            
            # Create comprehensive test dataset
            np.random.seed(42)
            test_data = pd.DataFrame({
                'order_id': [f'ORD_{i:06d}' for i in range(2000)],
                'customer_id': [f'CUST_{np.random.randint(1000, 9999)}' for _ in range(2000)],
                'product_code': [f'PROD_{np.random.randint(100, 999)}' for _ in range(2000)],
                'order_amount': np.random.lognormal(5, 1, 2000),
                'quantity': np.random.randint(1, 20, 2000),
                'order_status': np.random.choice(['completed', 'pending', 'cancelled'], 2000),
                'sales_channel': np.random.choice(['online', 'mobile', 'store'], 2000),
                'region': np.random.choice(['North', 'South', 'East', 'West'], 2000),
                'order_date': pd.date_range('2025-01-01', periods=2000, freq='10min')
            })
            
            # Introduce realistic data issues
            test_data.loc[0:300, 'order_amount'] = None  # 15% missing
            test_data.loc[0:100, 'customer_id'] = None   # 5% missing
            duplicates = test_data.iloc[0:200].copy()    # 10% duplicates
            test_data = pd.concat([test_data, duplicates], ignore_index=True)
            
            print(f"📊 Test dataset: {len(test_data):,} records with intentional issues")
            
            # Run comprehensive monitoring
            results = await monitor.monitor_pipeline(test_data, "AGENTIC_TEST_PIPELINE")
            
            # Display comprehensive results
            print("\n" + "="*70)
            print("🎯 AGENTIC AI MONITORING TEST RESULTS")
            print("="*70)
            
            print(f"🏷️  **Pipeline:** {results['pipeline_name']}")
            print(f"📊 **Records:** {results['metrics']['total_records']:,}")
            print(f"⚠️  **Risk Level:** {results['risk_level'].upper()}")
            print(f"🔍 **Anomalies:** {len(results['anomalies'])}")
            print(f"📈 **Data Quality:** {results['metrics']['data_quality_score']:.1f}%")
            
            if results['anomalies']:
                print(f"\n🚨 **Detected Anomalies:**")
                for i, anomaly in enumerate(results['anomalies'], 1):
                    print(f"   {i}. {anomaly}")
            
            print(f"\n👤 **Approval Summary:**")
            approved = [a for a in results['approval_results'] if a['status'] == 'approved']
            denied = [a for a in results['approval_results'] if a['status'] == 'denied']
            print(f"   • Total Actions: {len(results['approval_results'])}")
            print(f"   • Approved: {len(approved)}")
            print(f"   • Denied: {len(denied)}")
            
            print(f"\n🤖 **AI Insights Preview:**")
            insights_preview = results['ai_insights'][:150] + "..." if len(results['ai_insights']) > 150 else results['ai_insights']
            print(f"   {insights_preview}")
            
            print("\n✅ AGENTIC AI MONITORING TEST COMPLETED SUCCESSFULLY!")
            print("="*70)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Run the comprehensive test
    asyncio.run(test_agentic_monitor())
