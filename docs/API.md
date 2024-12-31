# Agentic Ideation System API Documentation

## Core Components

### 1. Agent Factory (`agents.py`)

#### `generate_dynamic_personas(role: str, topic: str) -> str`
Creates a specialized persona for an agent based on role and topic.

#### `create_focus_level_agents(config) -> Dict[str, Any]`
Creates agents for each focus level with proper counts.

#### `create_specialized_agents(agent_group, start_idx: int, group_type: str) -> Dict[str, Any]`
Creates specialized agents (analysis or deep dive) with proper counts.

#### `agent_factory(config) -> Dict[str, Any]`
Main factory function that creates all types of agents.

### 2. Task Generation (`utils/tasks.py`)

#### `generate_hierarchical_tasks(config: Config) -> dict`
Generates hierarchical tasks based on focus levels.

#### `load_config(file_path: str) -> Config`
Loads and validates configuration from YAML file.

### 3. Task Execution (`main.py`)

#### `execute_tasks(tasks, agents, prompts)`
Executes dynamically generated tasks with appropriate agents.

#### `save_intermediate_results(results, completed, total)`
Saves intermediate results during execution.

### 4. Result Synthesis (`synthesizer.py`)

#### `create_synthesizer_agent(topic: str)`
Creates an agent specialized in synthesizing results.

#### `analyze_results(results, config, topic, prompt)`
Analyzes and synthesizes all agent results.

## Data Structures

### 1. Configuration (`Config` class)
```python
class Config:
    topic: str
    focus_levels: List[FocusLevel]
    analysis_agents: List[AgentGroup]
    deep_dive_agents: List[AgentGroup]
    prompts: Prompts
```

### 2. Focus Level
```python
class FocusLevel:
    level_name: str
    focuses: List[str]
    num_agents: int
    parent_focus: Optional[str]
```

### 3. Agent Group
```python
class AgentGroup:
    level_name: str
    agent_types: List[AgentType]
```

### 4. Agent Type
```python
class AgentType:
    name: str
    focus: str
    num_agents: int
```

## Usage Examples

### 1. Creating Agents
```python
from agents import agent_factory
from utils import load_config

config = load_config("config/base_config.yaml")
agents = agent_factory(config)
```

### 2. Generating Tasks
```python
from utils import generate_hierarchical_tasks

tasks = generate_hierarchical_tasks(config)
```

### 3. Executing Tasks
```python
results = await execute_tasks(tasks, agents, config.prompts)
```

### 4. Synthesizing Results
```python
analysis = await analyze_results(results, config, config.topic, config.prompts.synthesizer)
```

## Error Handling

### 1. Configuration Validation
- Schema validation through Pydantic
- Type checking
- Required field verification

### 2. Runtime Errors
- Task execution errors
- Agent creation failures
- Result synthesis issues

### 3. Error Recovery
- Intermediate result saving
- Progress tracking
- Error logging

## Best Practices

### 1. Configuration
- Use explicit types
- Validate inputs
- Document changes

### 2. Agent Creation
- Balance agent distribution
- Match expertise to tasks
- Monitor performance

### 3. Task Execution
- Handle errors gracefully
- Save progress regularly
- Log important events

### 4. Result Synthesis
- Validate inputs
- Cross-reference findings
- Document assumptions

## Extension Points

### 1. New Agent Types
- Implement custom agent classes
- Add specialized behaviors
- Extend factory function

### 2. Custom Task Types
- Define new task structures
- Implement task generators
- Update execution logic

### 3. Result Processing
- Add custom analyzers
- Implement new synthesis methods
- Extend output formats
