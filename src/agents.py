"""
Agent factory and configuration module.
"""
from typing import Dict, Any, List
from utils import log_message

def generate_dynamic_personas(role: str, topic: str) -> str:
    """
    Generate a persona for an agent based on role and topic.
    """
    return f"You are a {role} specializing in {topic}. Provide actionable insights and expertise."

def create_focus_level_agents(config) -> Dict[str, Any]:
    """
    Create agents for each focus level with proper counts.
    """
    agents = {}
    agent_counter = 1
    
    for level in config.focus_levels:
        # Calculate base agents per focus and remaining agents
        base_agents_per_focus = level.num_agents // len(level.focuses)
        remaining_agents = level.num_agents % len(level.focuses)
        
        for i, focus in enumerate(level.focuses):
            # Add one extra agent to early focuses if there are remaining agents
            agents_for_this_focus = base_agents_per_focus + (1 if i < remaining_agents else 0)
            
            for j in range(agents_for_this_focus):
                agent_id = f"agent_{agent_counter}"
                agents[agent_id] = {
                    "name": f"Focus Agent {agent_counter}",
                    "persona": generate_dynamic_personas(focus, config.topic),
                    "model": "deepseek/deepseek-chat",
                    "type": "focus",
                    "level": level.level_name,
                    "focus_area": focus
                }
                agent_counter += 1
    
    return agents, agent_counter

def create_specialized_agents(agent_group, start_idx: int, group_type: str) -> Dict[str, Any]:
    """
    Create specialized agents (analysis or deep dive) with proper counts.
    """
    agents = {}
    agent_counter = start_idx
    
    for level in agent_group:
        for agent_type in level.agent_types:
            for i in range(agent_type.num_agents):
                agent_id = f"agent_{agent_counter}"
                agents[agent_id] = {
                    "name": f"{group_type} Agent {agent_counter}",
                    "persona": generate_dynamic_personas(agent_type.name, agent_type.focus),
                    "model": "deepseek/deepseek-chat",
                    "type": group_type,
                    "focus_area": agent_type.focus
                }
                agent_counter += 1
    
    return agents, agent_counter

def agent_factory(config) -> Dict[str, Any]:
    """
    Create all types of agents with proper counts and roles.
    """
    # Create focus level agents
    all_agents, next_idx = create_focus_level_agents(config)
    
    # Create analysis agents
    analysis_agents, next_idx = create_specialized_agents(
        config.analysis_agents, next_idx, "analysis"
    )
    all_agents.update(analysis_agents)
    
    # Create deep dive agents
    deep_dive_agents, _ = create_specialized_agents(
        config.deep_dive_agents, next_idx, "deep_dive"
    )
    all_agents.update(deep_dive_agents)
    
    log_message(f"Created {len(all_agents)} agents")
    return all_agents
