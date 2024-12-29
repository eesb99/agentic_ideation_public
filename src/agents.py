"""
Agent factory and configuration module.
"""
from typing import Dict, Any, List
from utils import log_message

def generate_dynamic_personas(topic: str, num_agents: int, focuses: List[str]) -> List[str]:
    """
    Generate personas dynamically for agents based on topic and roles.
    """
    personas = []
    for i in range(1, num_agents + 1):
        role = focuses[(i - 1) % len(focuses)]
        personas.append(f"You are a {role} specializing in {topic}. Provide actionable insights and expertise.")
    return personas

def agent_factory(num_agents: int, topic: str, focuses: List[str]) -> Dict[str, Any]:
    """
    Create agents dynamically with unique personas.
    """
    personas = generate_dynamic_personas(topic, num_agents, focuses)
    agents = {}
    for i in range(1, num_agents + 1):
        agents[f"agent_{i}"] = {
            "name": f"Agent {i}",
            "persona": personas[i - 1],
            "model": "deepseek/deepseek-chat"
        }
    return agents
