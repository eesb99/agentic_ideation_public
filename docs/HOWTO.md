# How to Use the Agentic Ideation System

## Quick Start Guide

1. **Environment Setup**
```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate agentic_ideation_public

# Create .env file
echo OPENROUTER_API_KEY=your_api_key_here > .env
```

2. **Configuration**
- Navigate to `src/config/base_config.yaml`
- Update the topic and focus areas
- Adjust agent numbers if needed
- Set model constraints (context window, max output, chunk size)

3. **Run the System**
```bash
cd src
python main.py
```

## Detailed Instructions

### 1. Configuration File Structure

The `base_config.yaml` has four main sections:

```yaml
1. topic: Your main research topic

2. focus_levels: Primary research areas
   - level_name
   - focuses
   - num_agents
   - parent_focus

3. analysis_agents: Cross-cutting analysis
   - name
   - focus
   - num_agents

4. deep_dive_agents: Detailed investigation
   - name
   - focus
   - num_agents
```

### 2. Agent Distribution

For optimal results:
- Focus Level Agents: 60-70% of total
- Analysis Agents: 15-20% of total
- Deep Dive Agents: 15-20% of total

### 3. Monitoring Progress

1. **Real-time Updates**
   - Task execution progress
   - Agent assignments
   - Completion status

2. **Intermediate Results**
   - Located in `temp/` directory
   - Updated every 10 tasks
   - Format: `intermediate_results_[N]of[Total]_[Timestamp].yaml`

3. **Discussion History**
   - Located in `config/output/discussion_history.json`
   - Contains all agent interactions
   - Useful for debugging

4. **Progress Tracking**
   - The system uses a gitignored `progress/` directory for:
     - Task completion status
     - Agent allocation tracking
     - Intermediate results
     - Performance metrics

### 4. Understanding Output

The final output in `output/[timestamp]/output.yaml` contains:

1. **Task Results**
   - Individual agent findings
   - Organized by focus area
   - Includes metadata

2. **Analysis Results**
   - Cross-cutting insights
   - Pattern identification
   - Trend analysis

3. **Deep Dive Results**
   - Detailed investigations
   - Specific focus areas
   - Technical details

4. **Synthesis**
   - Combined findings
   - Key insights
   - Recommendations

### 5. Best Practices

1. **Topic Definition**
   - Be specific and focused
   - Include clear scope
   - Define boundaries

2. **Focus Areas**
   - Use 5-7 primary areas
   - Ensure logical hierarchy
   - Avoid overlap

3. **Agent Distribution**
   - Balance workload
   - Match expertise to tasks
   - Consider dependencies

4. **Monitoring**
   - Check progress regularly
   - Review intermediate results
   - Verify agent performance

### 6. Troubleshooting

1. **Common Issues**
   - Memory usage
   - Task allocation
   - Agent coordination

2. **Solutions**
   - Adjust agent numbers
   - Check configuration
   - Review logs

### 7. Advanced Usage

1. **Custom Prompts**
   - Modify prompt templates
   - Add specific instructions
   - Include domain knowledge

2. **Output Analysis**
   - Use provided tools
   - Cross-reference results
   - Validate findings

3. **System Extension**
   - Add new agent types
   - Modify task allocation
   - Customize output format

## Environment Setup

### 1. Prerequisites
- Python 3.10
- Conda package manager
- Git (for version control)
- OpenRouter API key

### 2. Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic_ideation.git
cd agentic_ideation
```

2. Create the conda environment:
```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate agentic_ideation_public
```

3. Set up OpenRouter API:
```bash
# Create .env file
echo OPENROUTER_API_KEY=your_api_key_here > .env
```

4. Verify installation:
```bash
python -c "import pydantic, yaml, aiohttp, asyncio; print('Dependencies verified')"
```

## Configuration

### 1. Basic Configuration
Edit `src/config/base_config.yaml`:
```yaml
topic: "Your Analysis Topic"
focus_levels:
  - level_name: "Primary Research Areas"
    focuses:
      - "area1"
      - "area2"
    num_agents: 20
    parent_focus: null
```

### 2. Agent Configuration
Three types of agents:
1. **Focus Level Agents**
   - Distributed across focus areas
   - Balanced allocation using remainder distribution

2. **Analysis Agents**
   - Cross-cutting analysis
   - Configured in analysis_agents section

3. **Deep Dive Agents**
   - Specialized investigation
   - Configured in deep_dive_agents section

### 3. Model Constraints
Using OpenRouter's deepseek-chat:
- Context Window: 8K tokens
- Max Output: 4K tokens
- Chunk Size: 6K tokens (leaves room for prompts)

### 4. Progress Tracking
The system uses a gitignored `progress/` directory for:
- Task completion status
- Agent allocation tracking
- Intermediate results
- Performance metrics

## Running the System

### 1. Basic Execution
```bash
python src/main.py
```

### 2. Monitoring Progress
- Console output shows task execution
- Progress indicators for each stage
- Real-time agent discussions
- Check progress/ directory for details

### 3. Output Files
```
output/
├── YYYYMMDD_HHMMSS/
│   ├── output.yaml        # Final results
│   ├── discussion.json    # Agent discussions
│   └── intermediate/      # Checkpoint results
```

## Troubleshooting

### 1. Environment Issues
```bash
# Verify Python version
python --version  # Should be 3.10.x

# Update dependencies
conda env update -f environment.yml
```

### 2. Common Problems
1. **Memory Usage**
   - Reduce agent count in config
   - Monitor system resources
   - Check progress/memory_usage.log

2. **Task Distribution**
   - Check focus level configuration
   - Verify agent counts match tasks
   - Review progress/task_distribution.log

3. **Output Issues**
   - Check write permissions
   - Verify output directory exists
   - Check progress/error.log

## Best Practices

### 1. Configuration
- Keep agent counts balanced
- Use descriptive focus names
- Test configuration changes

### 2. Monitoring
- Watch task execution progress
- Check intermediate results
- Monitor system resources
- Review progress logs regularly

### 3. Output Management
- Review discussion history
- Backup important results
- Clean old output directories
- Archive progress logs

## Advanced Usage

### 1. Custom Agents
- Extend agent factory
- Add new agent types
- Customize agent behavior

### 2. Task Generation
- Modify task templates
- Add custom task types
- Adjust task distribution

### 3. Result Analysis
- Customize synthesis
- Add analysis metrics
- Export custom formats

## Dependencies
Core requirements (see environment.yml):
```yaml
dependencies:
  - python=3.10
  - pip
  - pip:
    - pyyaml>=6.0.1        # Configuration and output
    - aiohttp>=3.8.5       # Async HTTP client
    - asyncio>=3.4.3       # Async support
    - pydantic>=2.4.2      # Data validation
    - typing-extensions>=4.7.1  # Type hints
    - python-dotenv>=1.0.0  # Environment variables
    - colorama>=0.4.6      # Console colors
    - tqdm>=4.65.0         # Progress bars
    - rich>=13.5.2         # Rich console output
    - aiofiles>=23.2.1     # Async file operations
    - tenacity>=8.2.2      # Retry logic
