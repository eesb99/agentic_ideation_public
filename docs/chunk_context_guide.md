# Chunk Size and Context Management Guide

## Quick Reference
```python
DEEPSEEK_MAX_CONTEXT = 64 * 1024  # 64K tokens
OPTIMAL_CHUNK_SIZE = 8 * 1024     # 8K tokens per chunk
MAX_CHUNKS_PER_BATCH = 4          # 32K tokens per batch
```

## Context Window Management

### 1. Size Calculations
```python
class ContextConfig:
    def __init__(self):
        self.max_context_size = 64 * 1024    # DeepSeek limit
        self.chunk_size = 8 * 1024           # Single chunk
        self.batch_chunks = 4                # Chunks per batch
        self.overlap_tokens = 100            # Overlap between chunks
```

### 2. Chunk Processing Strategy

#### Safe Chunking
```python
def calculate_safe_chunks(total_tokens: int) -> int:
    """Calculate safe number of chunks for processing."""
    safe_chunk_size = 8 * 1024  # 8K tokens
    return math.ceil(total_tokens / safe_chunk_size)
```

#### Batch Assembly
```python
def create_batches(chunks: List[Chunk]) -> List[Batch]:
    """Create batches respecting context limits."""
    max_tokens_per_batch = 32 * 1024  # Half of context window
    current_batch_tokens = 0
    batches = []
    
    for chunk in chunks:
        if current_batch_tokens + chunk.size > max_tokens_per_batch:
            # Start new batch
            current_batch_tokens = 0
        current_batch_tokens += chunk.size
```

## Implementation in Our Codebase

### 1. Agent Configuration
```python
class AgentConfig:
    def __init__(self):
        # CPU-based settings
        self.agents_per_core = 2
        
        # Context-based settings
        self.max_tokens_per_agent = 32 * 1024
        self.chunks_per_batch = 4
        self.chunk_size = 8 * 1024
```

### 2. Safe Processing
```python
class AsyncAgentProcessor:
    async def process_with_context(self, items: List[Item]) -> List[Result]:
        # Calculate total tokens
        total_tokens = sum(item.token_count for item in items)
        
        # Determine safe batch size
        safe_batch_size = min(
            self.config.chunks_per_batch,
            (64 * 1024) // self.config.chunk_size
        )
        
        # Create batches
        batches = self._create_safe_batches(items, safe_batch_size)
```

## Memory and Performance

### 1. Token Budget
```python
class TokenBudget:
    def __init__(self, max_context: int = 64 * 1024):
        self.max_context = max_context
        self.safety_margin = 1024  # 1K token buffer
        
    def get_safe_chunk_size(self) -> int:
        return (self.max_context - self.safety_margin) // 8
```

### 2. Overlap Management
```python
def process_with_overlap(text: str, chunk_size: int, overlap: int = 100):
    """Process text with overlapping chunks for context continuity."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            # Find natural break point
            end = find_sentence_boundary(text, end)
        chunks.append(text[start:end])
        start = end - overlap
```

## Best Practices

### 1. Default Configuration
```python
def get_default_config():
    return {
        "chunk_size": 8 * 1024,      # 8K tokens
        "batch_size": 4,             # 4 chunks per batch
        "context_overlap": 100,      # 100 tokens overlap
        "safety_margin": 1024,       # 1K token buffer
    }
```

### 2. Monitoring
```python
class ContextMonitor:
    def __init__(self):
        self.total_tokens_processed = 0
        self.max_batch_tokens = 0
        
    def log_batch(self, batch_tokens: int):
        self.total_tokens_processed += batch_tokens
        self.max_batch_tokens = max(
            self.max_batch_tokens,
            batch_tokens
        )
```

## Practical Guidelines

### 1. Safe Limits
- Keep chunks ≤ 8K tokens
- Keep batches ≤ 32K tokens
- Maintain 1K token safety margin
- Use 100 token overlap

### 2. Performance Optimization
```python
# Good: Safe chunk size with overlap
chunk_size = 8 * 1024
overlap = 100

# Bad: Too large, risks context overflow
chunk_size = 16 * 1024  # Don't do this
```

### 3. Memory Management
```python
class MemoryManager:
    def __init__(self):
        self.max_tokens = 64 * 1024
        self.active_tokens = 0
        
    def can_process(self, tokens: int) -> bool:
        return self.active_tokens + tokens <= self.max_tokens
```

## Quick Decision Guide

1. **Single Item Processing**
   - Use 8K token chunks
   - Process sequentially
   - Maintain overlap

2. **Batch Processing**
   - Max 4 chunks per batch
   - Total ≤ 32K tokens
   - Monitor token count

3. **Parallel Processing**
   - Track per-agent tokens
   - Respect global limits
   - Balance load

## Key Takeaways

1. **Safe Sizes**
   - Chunks: 8K tokens
   - Batches: 32K tokens
   - Total: 64K context

2. **Optimization**
   - Use overlapping
   - Monitor token usage
   - Maintain buffers

3. **Implementation**
   - Track token counts
   - Handle overflows
   - Log usage stats
