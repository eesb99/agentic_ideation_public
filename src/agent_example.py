"""Example usage of the async agent processor with API calls."""
import asyncio
import random
from async_agent_processor import AsyncAgentProcessor, AgentConfig

async def simulate_api_call(item: dict) -> dict:
    """Simulate an API call with random latency and potential failures."""
    # Simulate API latency (100ms to 2s)
    await asyncio.sleep(random.uniform(0.1, 2.0))
    
    # Simulate occasional API failures (5% chance)
    if random.random() < 0.05:
        raise ConnectionError("API temporary failure")
    
    # Process the item
    return {
        "id": item["id"],
        "input": item["value"],
        "result": item["value"] * 2,
        "processed_by": "api"
    }

async def main():
    # Configure agent processor
    config = AgentConfig(
        agents_per_core=2,  # 2 agents per CPU core
        items_per_batch=5,  # Process 5 items per batch
        api_timeout=5.0,    # 5 second timeout for API calls
        max_retries=3,      # Retry failed calls 3 times
        retry_delay=1.0     # Wait 1 second between retries
    )
    
    processor = AsyncAgentProcessor[dict, dict](config)
    
    # Create test items
    items = [
        {"id": i, "value": i} 
        for i in range(50)
    ]
    
    print("Starting agent-based processing...")
    results = await processor.process_items(items, simulate_api_call)
    
    print(f"\nSuccessfully processed {len(results)} items")
    print("Sample results:", results[:3])

if __name__ == "__main__":
    asyncio.run(main())
