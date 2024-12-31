"""
Data models and schemas for the agentic ideation system.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in the discussion."""
    content: str = Field(..., description="The message content")
    role: str = Field(..., description="Role of the sender (user/assistant/system)")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the message was sent")


class Prompts(BaseModel):
    """System prompts configuration."""
    subtask_execution: str = Field(
        ...,
        description="Template for subtask execution prompts"
    )
    synthesizer: str = Field(
        ...,
        description="Template for synthesis prompts"
    )


class TaskFocusLevel(BaseModel):
    """Represents a level of task focuses with its agents."""
    level_name: str = Field(..., description="Name of this focus level")
    focuses: List[str] = Field(..., description="List of focuses at this level")
    num_agents: int = Field(gt=0, description="Number of agents at this level")
    parent_focus: Optional[str] = Field(None, description="Parent focus this level belongs to")


class AgentType(BaseModel):
    """Configuration for a specific type of agent."""
    name: str = Field(..., description="Name of the agent type")
    focus: str = Field(..., description="Focus area or specialty of this agent type")
    num_agents: int = Field(gt=0, description="Number of agents of this type")


class AgentGroup(BaseModel):
    """Configuration for a group of agents."""
    level_name: str = Field(..., description="Name of the agent group")
    agent_types: List[AgentType] = Field(..., description="Types of agents in this group")


class Config(BaseModel):
    """Main configuration for the task generation system."""
    topic: str = Field(
        ...,
        description="Main topic for task generation",
        min_length=5
    )
    focus_levels: List[TaskFocusLevel] = Field(
        ...,
        description="Hierarchical levels of task focuses"
    )
    analysis_agents: List[AgentGroup] = Field(
        ...,
        description="Configuration for analysis agents"
    )
    deep_dive_agents: List[AgentGroup] = Field(
        ...,
        description="Configuration for deep dive agents"
    )
    prompts: Prompts = Field(
        ...,
        description="System prompt templates"
    )


class Discussion(BaseModel):
    """Represents a complete discussion thread."""
    messages: List[Message] = Field(
        default_factory=list,
        description="List of messages in the discussion"
    )
    start_time: datetime = Field(
        default_factory=datetime.now,
        description="When the discussion started"
    )
    topic: str = Field(
        default="Task Generation and Execution",
        description="Topic of the discussion",
        min_length=5
    )
    max_messages: int = Field(
        default=50,
        description="Maximum number of messages to keep in history"
    )

    def prune_messages(self, max_tokens: int = 8000):
        """
        Prune messages to stay within token limits while keeping most relevant context.
        Args:
            max_tokens: Maximum tokens to allow (default 8000 to stay well under 16k limit)
        """
        if len(self.messages) > self.max_messages:
            # Keep first message for context and most recent messages
            self.messages = (
                self.messages[:1] +  # Keep first message
                self.messages[-(self.max_messages-1):]  # Keep recent messages
            )


Config.model_config = {
    'validate_assignment': True,
    'extra': 'forbid',
}