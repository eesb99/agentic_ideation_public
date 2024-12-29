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


class DeepDiveAgentType(BaseModel):
    """Configuration for a specific type of deep dive agent."""
    name: str = Field(..., description="Name of the agent type")
    focus: str = Field(..., description="Focus area or specialty of this agent type")
    num_agents: int = Field(gt=0, description="Number of agents of this type")


class DeepDiveLevel(BaseModel):
    """Configuration for deep dive analysis level."""
    level_name: str = Field(..., description="Name of the deep dive level")
    agent_types: List[DeepDiveAgentType] = Field(..., description="Types of agents at this level")


class Config(BaseModel):
    """Main configuration for the task generation system."""
    topic: str = Field(
        ...,
        description="The main topic or question to explore",
        min_length=10
    )
    focus_levels: List[TaskFocusLevel] = Field(
        ...,
        min_items=1,
        description="Hierarchical levels of task focuses"
    )
    prompts: Prompts = Field(
        ...,
        description="System prompts configuration"
    )
    deep_dive_agents: Optional[List[DeepDiveLevel]] = Field(
        None,
        description="Configuration for deep dive analysis agents"
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
        if len(self.messages) <= self.max_messages:
            return

        # Always keep the first message (original context/task)
        first_message = self.messages[0]
        
        # Keep the last N messages for recent context
        last_n = 10
        recent_messages = self.messages[-last_n:]
        
        # For remaining messages, prioritize:
        # 1. System messages (state changes)
        # 2. Longer messages (likely more important)
        middle_messages = self.messages[1:-last_n]
        prioritized = sorted(
            middle_messages,
            key=lambda m: (m.role == "system", len(m.content)),
            reverse=True
        )
        
        # Keep top messages up to max_messages - (1 + last_n)
        keep_count = self.max_messages - (1 + last_n)
        kept_middle = prioritized[:keep_count] if keep_count > 0 else []
        
        # Reassemble in chronological order
        self.messages = [first_message] + sorted(
            kept_middle + recent_messages,
            key=lambda m: m.timestamp
        )


Config.model_config = {
    'validate_assignment': True,
    'extra': 'forbid',
}