# AI Task-Agent System with DeepSeek V3

This project demonstrates an **AI-powered task-agent system** designed to scale up ideation and problem-solving using **DeepSeek V3 API**. The system dynamically creates tasks, assigns them to **100 virtual agents** with unique personas, and synthesizes the results into actionable insights.

- **Scale**: 100 agents working collaboratively for 24 hours.
- **Efficiency**: Processes **21 million tokens** for just $5.
- **Use Case**: Ideal for breaking down complex problems and exploring innovative solutions.

---

## **Features**

- **Dynamic Task Generation**: Creates tasks based on a configurable topic and scales to match the number of agents.
- **Contextual Agents**: Assigns tasks to agents with relevant personas (e.g., strategist, researcher, data analyst).
- **Scalable Summarization**: Synthesizes outputs from all agents into a cohesive final report.
- **Cost-Efficiency**: Uses **DeepSeek V3** to achieve large-scale processing at minimal cost.

---

## **File Structure**
```
.
├── config.yaml           # Configuration file for topic, task count, and prompts
├── main.py               # Main execution script
├── tasks.py              # Dynamic task generation
├── agents.py             # Agent and persona generation
├── synthesizer.py        # Synthesizer for summarizing results
├── api_utils.py          # API interaction logic
├── requirements.txt      # Python dependencies
├── environment.yml       # Conda environment configuration
├── output/               # Directory for generated outputs
│   ├── generated_config.yaml  # Output of tasks, agents, and summaries
```

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/ai-task-agent-system.git
cd ai-task-agent-system
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

### 3. Configure `config.yaml`
Set the main topic, number of tasks, and other parameters in the YAML file. Example:

```yaml
topic: "AI's role in climate change"
num_tasks: 100
```

### 4. Set the API Key
Ensure your **DeepSeek V3 API key** is securely stored in your OS environment variables. On Windows:
```bash
setx OPENROUTER_API_KEY "your_actual_api_key"
```

### 5. Run the Program
Execute the main script:
```bash
python main.py
```

### 6. Check Outputs
The generated tasks, agents, results, and summary will be saved to:
```
output/generated_config.yaml
```

---

## **FAQs**

### **1. What does this system do?**
This system dynamically generates tasks, assigns them to AI-powered virtual agents, and synthesizes the outputs into a cohesive report. It leverages the **DeepSeek V3 API** for scalable, cost-efficient AI processing.

### **2. How does it handle tasks and agents?**
The system:
1. Breaks down the main topic into smaller, contextual tasks.
2. Assigns each task to an agent with a relevant persona.
3. Processes tasks asynchronously and combines the results using a synthesizer agent.

### **3. How much does it cost to run?**
Using **DeepSeek V3**, processing 21 million tokens with 100 agents for 24 hours costs approximately **$5**.

### **4. Can I use this system for other topics?**
Absolutely! Just update the `topic` field in `config.yaml` to match your desired topic. The system will generate tasks and agents accordingly.

### **5. Is this scalable?**
Yes! The system can handle hundreds of tasks and agents dynamically. Adjust the `num_tasks` value in `config.yaml` to scale up or down.

### **6. What happens if an error occurs during a task?**
The system logs any errors and continues processing other tasks. The summary report will highlight incomplete or failed tasks.

### **7. Can I customize the personas or prompts?**
Yes! You can edit the `task_focuses` and `prompts` sections in `config.yaml` to tailor the system to your needs.

---

## **Dependencies**

### Environment Setup
- **Python 3.10** (via Conda)
- **Key Libraries**:
  - `httpx==0.24.1` - For asynchronous API requests
  - `pyyaml==6.0` - For YAML configuration and output handling
  - `pydantic>=2.0.0` - For data validation
  - `python-dotenv>=1.0.0` - For environment variables
  - `colorlog>=6.7.0` - For colored logging
  - `tqdm>=4.65.0` - For progress bars

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

## **Contact**

If you have questions or need help with this project, feel free to reach out! 🚀  

#DeepSeekV3 #AIAtScale #AffordableAI #InnovationOnABudget
