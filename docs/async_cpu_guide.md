# Understanding Async Agents and CPU Cores

## Quick Reference

```python
optimal_agents = cpu_cores * multiplier
# where multiplier is:
# - 1 for CPU-heavy work
# - 2-4 for API/IO work
```

## Why Async Matters

In our codebase, we use async for two main reasons:
1. Handle multiple API calls efficiently
2. Keep CPU cores busy while waiting

### The I/O Wait Problem
```python
# Synchronous code (bad)
for item in items:
    result = api_call(item)  # Waits doing nothing
    process(result)

# Async code (good)
async for item in items:
    result = await api_call(item)  # Other work continues
    process(result)
```

## How Our Agents Work

### 1. Agent Distribution
```python
class AsyncAgentProcessor:
    def __init__(self):
        self.cpu_cores = multiprocessing.cpu_count()
        self.total_agents = self.cpu_cores * 2  # For API work
```

When an agent makes an API call:
1. CPU is free to run other agents
2. No wasted CPU time
3. More concurrent API calls

### 2. Why Number of Agents Matters

#### Too Few Agents
```python
# 4 CPU cores, 2 agents total
# Result: CPUs sit idle during API calls
agents = cpu_cores * 0.5  # Underutilized
```

#### Too Many Agents
```python
# 4 CPU cores, 32 agents
# Result: System overhead, memory pressure
agents = cpu_cores * 8  # Overkill
```

#### Just Right
```python
# 4 CPU cores, 8-16 agents
# Result: Optimal throughput
agents = cpu_cores * (2 to 4)  # Sweet spot
```

## Our Implementation

### 1. API-Focused Design
```python
class AgentConfig:
    def __init__(self):
        self.agents_per_core = 2  # Default for API work
        self.items_per_batch = 10 # Small batches for APIs
```

Benefits:
- Constant API activity
- Efficient CPU usage
- Controlled concurrency

### 2. Batch Processing
```python
async def process_items(self, items: List[T]):
    batches = self._create_batches(items)
    # Each agent gets its own batches
    return await asyncio.gather(
        *[self._process_batch(batch) for batch in batches]
    )
```

### 3. Resource Management
```python
self.api_semaphore = asyncio.Semaphore(
    self.total_agents * 2  # Control concurrent API calls
)
```

## Real-World Examples

### 1. API Processing (4-Core CPU)

```python
# Configuration
config = AgentConfig(
    agents_per_core=2,     # 8 total agents
    items_per_batch=10,    # 80 items in flight
    api_timeout=30.0
)

# Processing 1000 items
# Without async: 1000 seconds (sequential)
# With async: ~125 seconds (parallel)
```

### 2. Mixed Workload

```python
# Morning: Heavy API load
config.agents_per_core = 3  # More concurrent API calls

# Evening: More CPU work
config.agents_per_core = 1  # Focus on processing
```

## Best Practices for Our Codebase

### 1. Starting Configuration
```python
def get_initial_config():
    return AgentConfig(
        agents_per_core=2,  # Conservative start
        items_per_batch=10, # Small batches
        api_timeout=30.0    # Standard timeout
    )
```

### 2. Monitoring
```python
async def _log_agent_stats(self):
    for agent_id, stats in self.agent_stats.items():
        logger.info(
            f"Agent {agent_id}: "
            f"Processed={stats.processed}, "
            f"API Time={stats.total_api_time}s"
        )
```

### 3. Adjustment Strategy
```python
def adjust_agents(self, api_latency: float):
    if api_latency > 1.0:
        self.agents_per_core = min(4, self.agents_per_core + 1)
    elif api_latency < 0.1:
        self.agents_per_core = max(1, self.agents_per_core - 1)
```

## Quick Decision Guide

1. **API-Heavy Work**
   - Use `cores * 2` agents
   - Small batches
   - Monitor API latency

2. **CPU-Heavy Work**
   - Use `cores * 1` agents
   - Larger batches
   - Watch CPU usage

3. **Mixed Workload**
   - Start with `cores * 2`
   - Adjust based on metrics
   - Balance batch sizes

## Key Takeaways

1. **Async + Agents = Efficient**
   - CPU stays busy
   - API calls overlap
   - Better throughput

2. **Right-Size Agents**
   - Match workload type
   - Consider API limits
   - Monitor and adjust

3. **Our Sweet Spot**
   - 2-3 agents per core
   - 10-item batches
   - Semaphore control
