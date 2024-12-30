# AI Task-Agent System with DeepSeek V3

This project demonstrates an **AI-powered task-agent system** designed to scale up ideation and problem-solving using **DeepSeek V3 API** (via OpenRouter). The system dynamically creates tasks, assigns them to **100 virtual agents** with unique personas, and synthesizes the results into actionable insights.

- **Scale**: 100 agents working collaboratively
- **Efficiency**: Optimized token usage and parallel processing
- **Use Case**: Ideal for breaking down complex problems and exploring innovative solutions.

## **Version**

Current version: **0.1.1**
- Enhanced error handling and logging in synthesizer
- Improved real-time progress reporting
- Better task result processing

---

## **Features**

- **Dynamic Task Generation**: Creates tasks based on a configurable topic and scales to match the number of agents.
- **Contextual Agents**: Assigns tasks to agents with relevant personas (e.g., strategist, researcher, data analyst).
- **Scalable Summarization**: Synthesizes outputs from all agents into a cohesive final report.
- **Real-time Progress**: Shows detailed progress and results in real-time.
- **Robust Error Handling**: Comprehensive error handling and recovery mechanisms.

---

## **Dependencies**

### Core Dependencies
```
python>=3.8
pydantic>=2.0.0
pyyaml>=6.0.1
aiohttp>=3.8.0
asyncio>=3.4.3
```

### Development Dependencies
```
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
```

### API Requirements
- OpenRouter API access for DeepSeek V3
- Valid OpenRouter API key

---

## **File Structure**
```
.
├── config/
│   ├── base_config.yaml    # Base configuration settings
│   └── output/             # Generated outputs and logs
├── src/
│   ├── __init__.py        # Package initialization and version
│   ├── main.py            # Main execution script
│   ├── agents.py          # Agent and persona generation
│   ├── synthesizer.py     # Results synthesis and analysis
│   └── utils/
│       ├── api_utils.py   # API interaction logic
│       ├── tasks.py       # Task generation
│       └── schemas.py     # Data models and validation
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── environment.yml       # Conda environment configuration
```

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone https://github.com/eesb99/agentic_ideation.git
cd agentic_ideation
```

### 2. Environment Setup
#### Option 1: Install with Conda (Recommended)
```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate agentic_ideation
```

#### Option 2: Install with pip
```bash
pip install -r requirements.txt
```

### 3. Configure Settings
Set the main topic and parameters in `config/base_config.yaml`:

```yaml
topic: "Your research topic"
focus_levels:
  - level_name: "Strategic"
    focuses: ["Market Analysis", "Technology Trends"]
    num_agents: 3
```

### 4. Set the API Key
Store your OpenRouter API key in environment variables:
```bash
# Windows
setx OPENROUTER_API_KEY "your_api_key"

# Linux/Mac
export OPENROUTER_API_KEY="your_api_key"
```

### 5. Run the Program
```bash
python -m src.main
```

---

## **Future Improvements**

### Short-term (v0.2.0)
1. **Performance Optimization**
   - Implement parallel task processing
   - Add caching for API responses
   - Optimize token usage

2. **Enhanced Monitoring**
   - Add detailed progress visualization
   - Implement task execution metrics
   - Create interactive progress dashboard

3. **Error Recovery**
   - Add automatic retry mechanisms
   - Implement checkpoint/resume functionality
   - Add partial results recovery

### Medium-term (v0.3.0)
1. **Advanced Analysis**
   - Add sentiment analysis of results
   - Implement cross-reference between tasks
   - Add statistical analysis of outputs

2. **Integration Features**
   - Add REST API interface
   - Support multiple LLM providers
   - Add export to various formats

3. **Quality Improvements**
   - Add automated testing pipeline
   - Implement result validation
   - Add quality scoring system

### Long-term (v1.0.0)
1. **AI Enhancements**
   - Self-optimizing agent system
   - Dynamic prompt generation
   - Adaptive task allocation

2. **Scalability**
   - Distributed processing support
   - Cloud deployment options
   - Horizontal scaling capability

3. **Enterprise Features**
   - Multi-user support
   - Access control system
   - Audit logging

---

## **FAQs**

### **1. What does this system do?**
This system dynamically generates tasks, assigns them to AI-powered virtual agents, and synthesizes the outputs into a cohesive report. It leverages the **DeepSeek V3 API** (via OpenRouter) for scalable AI processing.

### **2. How does it handle tasks and agents?**
The system:
1. Breaks down the main topic into smaller, contextual tasks.
2. Assigns each task to an agent with a relevant persona.
3. Processes tasks asynchronously and combines the results using a synthesizer agent.

### **3. What are the costs involved?**
The cost varies based on your usage and the current OpenRouter API pricing for DeepSeek V3. We recommend checking the [OpenRouter pricing page](https://openrouter.ai/pricing) for the most up-to-date rates.

### **4. Can I use this system for other topics?**
Absolutely! Just update the `topic` field in `config/base_config.yaml` to match your desired topic. The system will generate tasks and agents accordingly.

### **5. Is this scalable?**
Yes! The system can handle hundreds of tasks and agents dynamically. Adjust the `num_agents` value in `config/base_config.yaml` to scale up or down.

### **6. What happens if an error occurs during a task?**
The system logs any errors and continues processing other tasks. The summary report will highlight incomplete or failed tasks.

### **7. Can I customize the personas or prompts?**
Yes! You can edit the `focus_levels` section in `config/base_config.yaml` to tailor the system to your needs.

---

## **Example Outputs**

### **Generated Tasks**
```yaml
tasks:
  task_1: "Task 1: Focus on analyzing trends in relation to AI's role in climate change. Provide detailed insights."
  task_2: "Task 2: Focus on identifying challenges in relation to AI's role in climate change. Provide detailed insights."
  ...
```

### **Generated Agents**
```yaml
agents:
  agent_1:
    name: "Agent 1"
    persona: "You are a Data Analyst specializing in AI's role in climate change. Provide actionable insights and expertise."
    model: "deepseek/deepseek/chat"
  ...
```

### **Summary**
```yaml
summary:
  executive_summary: "AI is revolutionizing climate change mitigation by optimizing renewable energy and forecasting natural disasters."
  detailed_analysis: |
    Task 1 focused on analyzing trends, revealing AI's role in improving energy grid efficiency.
    Task 2 highlighted challenges in integrating AI with existing infrastructure.
    Task 3 proposed solutions like predictive models for disaster risk reduction.
  recommendations: |
    1. Invest in AI research for sustainable energy solutions.
    2. Develop cross-industry standards for AI in environmental projects.
    3. Foster collaboration between governments, AI developers, and climate experts.
```

---

## **Contributing**

We welcome contributions! Please fork the repository at [https://github.com/eesb99/agentic_ideation](https://github.com/eesb99/agentic_ideation) and submit your pull requests.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- OpenRouter team for providing the API
- DeepSeek team for providing the V3 API
- Contributors and testers
- Open source community

---

## **Contact**

If you have questions or need help with this project, feel free to reach out via [GitHub Issues](https://github.com/eesb99/agentic_ideation/issues)! 🚀  

#OpenRouter #DeepSeekV3 #AIAtScale #AffordableAI #InnovationOnABudget
