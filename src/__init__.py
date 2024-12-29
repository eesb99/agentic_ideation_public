"""
Agentic Ideation - A framework for AI-driven task generation and execution.
"""

from .utils import (
    make_api_call,
    Config,
    Discussion,
    Message,
    Prompts,
    load_config,
    generate_unique_tasks,
    save_to_yaml,
    log_message
)
from .agents import agent_factory
from .synthesizer import create_synthesizer_agent, summarize_results

__version__ = '0.1.0'
__all__ = [
    'make_api_call',
    'Config',
    'Discussion',
    'Message',
    'Prompts',
    'load_config',
    'generate_unique_tasks',
    'save_to_yaml',
    'log_message',
    'agent_factory',
    'create_synthesizer_agent',
    'summarize_results'
]
