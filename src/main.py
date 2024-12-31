#!/usr/bin/env python3
"""
Main entry point for the agentic ideation system.
"""

import asyncio
import os
import yaml
import json
from datetime import datetime
from utils import (
    load_config,
    generate_hierarchical_tasks,
    save_to_yaml,
    make_api_call,
    log_message
)
from agents import agent_factory
from synthesizer import create_synthesizer_agent, summarize_results, analyze_results

class DiscussionLogger:
    def __init__(self):
        self.history = []
        self.output_dir = "config/output"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def add_entry(self, entry):
        """Add a new discussion entry with real-time output"""
        self.history.append(entry)
        print("\n[DISCUSSION] New entry added")
        print(json.dumps(entry, indent=2))
        self.save_history()
        
    def save_history(self):
        """Save full discussion history"""
        history_file = os.path.join(self.output_dir, "discussion_history.json")
        print(f"\n[SAVING] Discussion history to {history_file}")
        
        with open(history_file, "w") as f:
            json.dump(self.history, f, indent=2)
        print("[SAVED] Discussion history updated\n")

# Initialize the discussion logger
discussion_logger = DiscussionLogger()

async def execute_tasks(tasks, agents, prompts, config):
    """
    Execute dynamically generated tasks with agents.
    """
    results = {}
    task_list = []
    
    # Calculate total tasks across all levels and agent types
    focus_tasks = sum(len(focus_tasks) for level_tasks in tasks.values() for focus_tasks in level_tasks.values())
    analysis_tasks = sum(sum(agent_type.num_agents for agent_type in group.agent_types) 
                        for group in config.analysis_agents)
    deep_dive_tasks = sum(sum(agent_type.num_agents for agent_type in group.agent_types) 
                         for group in config.deep_dive_agents)
    total_tasks = focus_tasks + analysis_tasks + deep_dive_tasks
    
    log_message(f"Starting execution of {total_tasks} tasks ({focus_tasks} focus, {analysis_tasks} analysis, {deep_dive_tasks} deep dive)...", "info")
    print(f"\n[STARTING] Task execution")
    print(f"[TOTAL] {total_tasks} tasks to process\n")
    
    # Process focus level tasks
    for level_name, level_tasks in tasks.items():
        for focus, focus_tasks in level_tasks.items():
            # Find agents for this focus and level
            focus_agents = [
                (aid, a) for aid, a in agents.items()
                if a['type'] == 'focus' and a['level'] == level_name and a['focus_area'] == focus
            ]
            
            for task_id, task_description in focus_tasks.items():
                # Get the next available agent for this focus
                if focus_agents:
                    agent_id, agent = focus_agents.pop(0)
                    log_message(f"Dispatching {task_id} to {agent['name']}", "system")
                    
                    subtask_prompt = prompts.subtask_execution.format(
                        persona=agent["persona"],
                        subtask=task_description
                    )
                    
                    task_list.append({
                        "task": asyncio.create_task(
                            make_api_call(
                                [{"role": "user", "content": subtask_prompt}],
                                agent["model"],
                                f"Executing {task_id} with {agent['name']}"
                            )
                        ),
                        "key": task_id,
                        "agent": agent['name'],
                        "level": level_name,
                        "focus": focus
                    })
    
    # Process analysis and deep dive agents
    for agent_id, agent in agents.items():
        if agent['type'] in ['analysis', 'deep_dive']:
            task_id = f"{agent['type']}_{agent_id}"
            subtask_prompt = prompts.subtask_execution.format(
                persona=agent["persona"],
                subtask=f"Analyze {agent['focus_area']} for the topic: {config.topic}"
            )
            
            task_list.append({
                "task": asyncio.create_task(
                    make_api_call(
                        [{"role": "user", "content": subtask_prompt}],
                        agent["model"],
                        f"Executing {task_id} with {agent['name']}"
                    )
                ),
                "key": task_id,
                "agent": agent['name'],
                "level": agent['type'],
                "focus": agent['focus_area']
            })

    # Process results
    completed = 0
    for task_info in task_list:
        try:
            result = await task_info["task"]
            if result:
                if task_info["level"] not in results:
                    results[task_info["level"]] = {}
                if task_info["focus"] not in results[task_info["level"]]:
                    results[task_info["level"]][task_info["focus"]] = {}
                results[task_info["level"]][task_info["focus"]][task_info["key"]] = result
                completed += 1
                log_message(f"Task {task_info['key']} completed successfully with {task_info['agent']} ({completed}/{total_tasks})", "success")
            else:
                log_message(f"Task {task_info['key']} failed with {task_info['agent']}", "error")
        except Exception as e:
            log_message(f"Error in task {task_info['key']}: {str(e)}", "error")
        
        # Save intermediate results every 10 tasks
        if completed % 10 == 0:
            await save_intermediate_results(results, completed, total_tasks)
        
        # Log the discussion
        discussion_logger.add_entry({
            "task": task_info["key"],
            "agent": task_info["agent"],
            "result": result
        })
    
    return results

async def save_intermediate_results(results, completed, total):
    """Save intermediate results to a temporary file with real-time output"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    intermediate_file = os.path.join("temp", f"intermediate_results_{completed}of{total}_{timestamp}.yaml")
    os.makedirs("temp", exist_ok=True)
    
    print(f"\n[SAVING] Intermediate results ({completed}/{total})")
    print(f"[PATH] {intermediate_file}")
    print("[CONTENT]")
    print(yaml.dump(results))
    
    with open(intermediate_file, "w") as f:
        yaml.dump(results, f)
    print(f"[SAVED] File written successfully\n")

def save_to_yaml(data, file_path):
    """Save output with real-time display"""
    print("\n[SAVING] Output data")
    print("[CONTENT]")
    print(yaml.dump(data))
    
    with open(file_path, "w") as f:
        yaml.dump(data, f)
    print(f"[SAVED] Output written to {file_path}\n")

async def main():
    print("\n[STARTING] Agentic Ideation System")
    print("[TIME] " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    log_message("Loading configuration...", "info")
    # Get the absolute path to the config file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config", "base_config.yaml")
    config = load_config(config_path)
    
    print("\n[CONFIG] Loaded configuration")
    print(yaml.dump(config))
    
    topic = config.topic
    # Calculate total agents from all types
    focus_agents = sum(level.num_agents for level in config.focus_levels)
    analysis_agents = sum(sum(agent.num_agents for agent in group.agent_types) for group in config.analysis_agents)
    deep_dive_agents = sum(sum(agent.num_agents for agent in group.agent_types) for group in config.deep_dive_agents)
    total_agents = focus_agents + analysis_agents + deep_dive_agents
    
    log_message(f"Total agents: {total_agents} ({focus_agents} focus, {analysis_agents} analysis, {deep_dive_agents} deep dive)", "info")
    log_message("Generating hierarchical tasks and creating agents...", "info")
    tasks = generate_hierarchical_tasks(config)
    agents = agent_factory(config)

    log_message("Starting task execution...", "info")
    results = await execute_tasks(tasks, agents, config.prompts, config)

    log_message("Creating synthesizer agent...", "info")
    synthesizer_agent = create_synthesizer_agent(topic)
    
    log_message("Starting result synthesis...", "info")
    analysis_results = await analyze_results(results, config, topic, config.prompts.synthesizer)

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Save final results
    log_message("Saving final results...", "info")
    save_to_yaml(
        {
            "tasks": tasks,
            "agents": agents,
            "results": results,
            "initial_summary": analysis_results["initial_summary"],
            "deep_dive_analysis": analysis_results["deep_dive_analysis"]
        },
        os.path.join(output_dir, "output.yaml")
    )
    
    log_message("Process completed successfully!", "success")
    print("\nInitial Summary:")
    print("=" * 80)
    print(analysis_results["initial_summary"])
    print("\nDeep Dive Analysis:")
    print("=" * 80)
    print(analysis_results["deep_dive_analysis"])
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
