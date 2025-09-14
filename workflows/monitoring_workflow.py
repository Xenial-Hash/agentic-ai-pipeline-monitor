# workflows/monitoring_workflow.py - Main Monitoring Workflow
import asyncio
from agno import Workflow
from agents.pipeline_monitor_agent import PipelineMonitorAgent
from config.database import test_connection

class MonitoringWorkflow(Workflow):
    def __init__(self):
        super().__init__()
        self.monitor_agent = PipelineMonitorAgent()
    
    async def run_complete_monitoring(self, data_source):
        """Run complete monitoring workflow"""
        
        print("🚀 AGNO MONITORING WORKFLOW STARTED")
        print("="*60)
        
        # Step 1: Test MySQL connection
        if not test_connection():
            raise Exception("MySQL connection failed")
        
        # Step 2: Load data
        df = await self.load_data(data_source)
        
        # Step 3: Run monitoring
        results = await self.monitor_agent.monitor_pipeline(df, "ProductionPipeline")
        
        print("✅ AGNO MONITORING WORKFLOW COMPLETED")
        return results
    
    async def load_data(self, data_source):
        """Load data from various sources"""
        if isinstance(data_source, str) and data_source.endswith('.csv'):
            return pd.read_csv(data_source)
        elif isinstance(data_source, pd.DataFrame):
            return data_source
        else:
            # Generate sample data
            import pandas as pd
            import numpy as np
            return pd.DataFrame({
                'transaction_id': range(1000),
                'amount': np.random.normal(500, 100, 1000),
                'status': np.random.choice(['active', 'inactive'], 1000, p=[0.9, 0.1])
            })