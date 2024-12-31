"""Asynchronous Agent-Based Batch Processor.

Efficiently manages multiple agents for batch processing with API calls,
automatically scaling based on available CPU cores.
"""
import asyncio
import multiprocessing
from typing import List, Any, Callable, TypeVar, Generic, Coroutine, Dict
from dataclasses import dataclass
import logging
import time
from contextlib import asynccontextmanager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variables for generic processing
T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type

@dataclass
class AgentConfig:
    """Configuration for agent-based processing."""
    cpu_cores: int = multiprocessing.cpu_count()
    agents_per_core: int = 2  # Adjust based on IO vs CPU intensity
    items_per_batch: int = 10
    api_timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0

@dataclass
class AgentStats:
    """Track agent processing statistics."""
    agent_id: int
    processed: int = 0
    failed: int = 0
    api_calls: int = 0
    total_api_time: float = 0.0

class AsyncAgentProcessor(Generic[T, R]):
    """Manages multiple agents for efficient batch processing with API calls."""

    def __init__(self, config: AgentConfig = None):
        """Initialize the agent processor.
        
        Args:
            config: Configuration for agent processing
        """
        self.config = config or AgentConfig()
        self.total_agents = self.config.cpu_cores * self.config.agents_per_core
        self.agent_stats: Dict[int, AgentStats] = {
            i: AgentStats(agent_id=i) for i in range(self.total_agents)
        }
        self.api_semaphore = asyncio.Semaphore(self.total_agents * 2)
        logger.info(f"Initialized {self.total_agents} agents across {self.config.cpu_cores} CPU cores")

    @asynccontextmanager
    async def _api_call_context(self, agent_id: int):
        """Context manager for tracking API calls."""
        start_time = time.time()
        try:
            async with self.api_semaphore:
                yield
        finally:
            duration = time.time() - start_time
            self.agent_stats[agent_id].api_calls += 1
            self.agent_stats[agent_id].total_api_time += duration

    async def _process_with_retry(
        self,
        agent_id: int,
        item: T,
        processor: Callable[[T], Coroutine[Any, Any, R]]
    ) -> R:
        """Process an item with retry logic."""
        for attempt in range(self.config.max_retries):
            try:
                async with self._api_call_context(agent_id):
                    async with asyncio.timeout(self.config.api_timeout):
                        result = await processor(item)
                        self.agent_stats[agent_id].processed += 1
                        return result
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    self.agent_stats[agent_id].failed += 1
                    logger.error(f"Agent {agent_id} failed to process item after {self.config.max_retries} attempts: {str(e)}")
                    raise
                await asyncio.sleep(self.config.retry_delay * (attempt + 1))

    async def _agent_process_batch(
        self,
        agent_id: int,
        batch: List[T],
        processor: Callable[[T], Coroutine[Any, Any, R]]
    ) -> List[R]:
        """Process a batch of items with a single agent."""
        results = []
        for item in batch:
            try:
                result = await self._process_with_retry(agent_id, item, processor)
                results.append(result)
            except Exception as e:
                logger.error(f"Agent {agent_id} failed to process item: {str(e)}")
        return results

    async def process_items(
        self,
        items: List[T],
        processor: Callable[[T], Coroutine[Any, Any, R]]
    ) -> List[R]:
        """Process items using multiple agents.
        
        Args:
            items: List of items to process
            processor: Async function to process each item
            
        Returns:
            List of successfully processed results
        """
        # Split items into batches for agents
        batches: List[List[T]] = []
        for i in range(0, len(items), self.config.items_per_batch):
            batch = items[i:i + self.config.items_per_batch]
            batches.append(batch)

        # Distribute batches across agents
        tasks = []
        for i, batch in enumerate(batches):
            agent_id = i % self.total_agents
            task = self._agent_process_batch(agent_id, batch, processor)
            tasks.append(task)

        # Process all batches and collect results
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        results: List[R] = []
        
        for batch_result in batch_results:
            if isinstance(batch_result, Exception):
                logger.error(f"Batch processing error: {str(batch_result)}")
                continue
            results.extend(batch_result)

        self._log_stats()
        return results

    def _log_stats(self) -> None:
        """Log processing statistics for all agents."""
        total_processed = sum(stat.processed for stat in self.agent_stats.values())
        total_failed = sum(stat.failed for stat in self.agent_stats.values())
        total_api_calls = sum(stat.api_calls for stat in self.agent_stats.values())
        total_api_time = sum(stat.total_api_time for stat in self.agent_stats.values())

        logger.info(
            f"\nProcessing Statistics:"
            f"\nTotal Agents: {self.total_agents}"
            f"\nTotal Processed: {total_processed}"
            f"\nTotal Failed: {total_failed}"
            f"\nTotal API Calls: {total_api_calls}"
            f"\nAverage API Time: {total_api_time/total_api_calls:.2f}s"
        )

        for agent_id, stats in self.agent_stats.items():
            logger.info(
                f"\nAgent {agent_id}:"
                f"\n  Processed: {stats.processed}"
                f"\n  Failed: {stats.failed}"
                f"\n  API Calls: {stats.api_calls}"
                f"\n  Avg API Time: {stats.total_api_time/stats.api_calls:.2f}s"
            )
