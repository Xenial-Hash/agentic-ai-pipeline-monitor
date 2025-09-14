# main.py - Main Application Entry Point
import asyncio
import pandas as pd
from workflows.monitoring_workflow import MonitoringWorkflow
from config.database import test_connection

async def main():
    print("🚀 AGNO AGENTIC AI PIPELINE MONITOR")
    print("🎯 MySQL + Human-in-the-Loop Enabled")
    print("="*60)
    
    # Test database connection
    if not test_connection():
        print("❌ Please check your MySQL configuration in .env file")
        return
    
    # Initialize workflow
    workflow = MonitoringWorkflow()
    
    # Run monitoring with sample data
    results = await workflow.run_complete_monitoring("data/sample_data.csv")
    
    print("\n📋 MONITORING COMPLETED")
    print(f"Pipeline Health: {results.get('risk_level', 'unknown')}")
    print(f"Anomalies: {len(results.get('anomalies', [])}")

if __name__ == "__main__":
    asyncio.run(main())