import yaml
from datetime import datetime
import os
from utils.schemas import Config, Discussion, Message
import json
from typing import List

def load_config(file_path: str) -> Config:
    """
    Load and validate configuration from a YAML file.
    Returns a validated Config object.
    """
    with open(file_path, "r") as file:
        config_dict = yaml.safe_load(file)
    return Config(**config_dict)

def generate_hierarchical_tasks(config: Config) -> dict:
    """
    Generate hierarchical tasks based on focus levels.
    Returns a nested dictionary of tasks organized by levels and focuses.
    """
    tasks = {}
    
    # Process each focus level
    for level in config.focus_levels:
        level_tasks = {}
        
        # Calculate base tasks per focus and remaining tasks
        base_tasks_per_focus = level.num_agents // len(level.focuses)
        remaining_tasks = level.num_agents % len(level.focuses)
        
        # Generate tasks for each focus in this level
        for i, focus in enumerate(level.focuses):
            focus_tasks = {}
            # Add one extra task to early focuses if there are remaining tasks
            tasks_for_this_focus = base_tasks_per_focus + (1 if i < remaining_tasks else 0)
            
            for j in range(tasks_for_this_focus):
                task_id = f"{level.level_name}_{focus}_{j+1}".lower().replace(" ", "_")
                task_description = (
                    f"Focus: {focus} within {level.level_name}\n"
                    f"Parent Focus: {level.parent_focus if level.parent_focus else 'Root'}\n"
                    f"Task: Analyze and provide insights for {config.topic}"
                )
                focus_tasks[task_id] = task_description
            
            level_tasks[focus] = focus_tasks
            
        tasks[level.level_name] = level_tasks
        
        # Log task generation
        log_message(f"Generated {sum(len(ft) for ft in level_tasks.values())} tasks for {level.level_name}")
    
    return tasks

def save_to_yaml(data: dict, file_path: str) -> str:
    """
    Save data to a YAML file.
    Returns the path of the saved file.
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(file_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False)
    
    log_message(f"Saved data to {file_path}")
    return file_path

def log_message(content: str, role: str = "system") -> None:
    """
    Log a message to console and optionally to discussion history.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Define emoji indicators for different message types
    indicators = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "system": "🔄",
        "user": "👤",
        "assistant": "🤖"
    }
    
    indicator = indicators.get(role, "📝")
    print(f"[{timestamp}] {indicator} {content}")
