-- SQL Server version of the database setup
CREATE DATABASE agentic_pipeline_monitor;
GO

USE agentic_pipeline_monitor;
GO

-- Agent storage table (SQL Server syntax)
CREATE TABLE agent_storage (
    id INT IDENTITY(1,1) PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    data NVARCHAR(MAX) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);

-- Agent memory table (SQL Server syntax)
CREATE TABLE agent_memory (
    id INT IDENTITY(1,1) PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    memory_type VARCHAR(100) NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Approval requests table (SQL Server syntax)
CREATE TABLE approval_requests (
    id INT IDENTITY(1,1) PRIMARY KEY,
    action_type VARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    decision NVARCHAR(MAX) NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    decided_at DATETIME2 NULL
);

-- Pipeline monitoring history (SQL Server syntax)
CREATE TABLE monitoring_history (
    id INT IDENTITY(1,1) PRIMARY KEY,
    pipeline_name VARCHAR(255) NOT NULL,
    metrics NVARCHAR(MAX) NOT NULL,
    anomalies NVARCHAR(MAX) NULL,
    risk_level VARCHAR(50) NULL,
    ai_insights NVARCHAR(MAX) NULL,
    execution_results NVARCHAR(MAX) NULL,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Create indexes for performance
CREATE INDEX idx_agent_storage_agent_id ON agent_storage(agent_id);
CREATE INDEX idx_agent_memory_agent_id ON agent_memory(agent_id);
CREATE INDEX idx_approval_status ON approval_requests(status);
CREATE INDEX idx_monitoring_pipeline ON monitoring_history(pipeline_name);

-- Verify tables were created
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';