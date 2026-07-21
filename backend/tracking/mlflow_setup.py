import mlflow
from backend.config import settings

def setup_mlflow():
    """Initialize MLflow tracking"""
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
    print(f"✅ MLflow tracking initialized at {settings.MLFLOW_TRACKING_URI}")
    return mlflow

def log_agent_performance(agent_name: str, metrics: dict, params: dict = None):
    """Log agent performance metrics"""
    with mlflow.start_run(run_name=f"{agent_name}_run"):
        # Log parameters
        if params:
            mlflow.log_params(params)
        
        # Log metrics
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
        
        # Log model (if applicable)
        # mlflow.langchain.log_model(...)
        
        run_id = mlflow.active_run().info.run_id
        print(f"✅ Logged metrics for {agent_name} - Run ID: {run_id}")
        return run_id

if __name__ == "__main__":
    setup_mlflow()