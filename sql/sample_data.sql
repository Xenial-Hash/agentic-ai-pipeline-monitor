-- sql/sample_data.sql - Sample Data Insertion for SQL Server

-- Insert sample data into agent_storage
INSERT INTO agent_storage (agent_id, data) VALUES
('agent_1', '{"key": "value"}'),
('agent_2', '{"key": "value"}');

-- Insert sample data into agent_memory
INSERT INTO agent_memory (agent_id, memory_type, content) VALUES
('agent_1', 'short_term', '{"memory": "short term data"}'),
('agent_2', 'long_term', '{"memory": "long term data"}');

-- Insert sample data into approval_requests
INSERT INTO approval_requests (action_type, description, risk_level, status) VALUES
('action_1', 'Description for action 1', 'low', 'pending'),
('action_2', 'Description for action 2', 'high', 'approved');

-- Insert sample data into monitoring_history
INSERT INTO monitoring_history (pipeline_name, metrics, anomalies, risk_level, ai_insights, execution_results) VALUES
('Pipeline1', '{"metric1": 100, "metric2": 200}', '["Anomaly1", "Anomaly2"]', 'medium', 'AI insights here', '{"result": "success"}');