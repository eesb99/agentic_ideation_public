# Contributing Guidelines

## Code Standards

### 1. Agent and Task Distribution
When distributing agents or tasks across focuses:
```python
# Calculate base and remaining items
base_per_focus = total_items // num_focuses
remaining_items = total_items % num_focuses

# Distribute items
for i, focus in enumerate(focuses):
    # Add one extra item to early focuses if there are remaining items
    items_for_this_focus = base_per_focus + (1 if i < remaining_items else 0)
```

This ensures:
- Even distribution of items (agents/tasks) across focuses
- Proper handling of remainders
- Consistent agent-to-task mapping

### 2. Code Organization
- Keep related functionality together
- Use clear, descriptive variable names
- Follow Python PEP 8 style guide
- Maximum line length: 88 characters (Black formatter)
- Use type hints for function parameters and returns

### 3. Error Handling
- Use proper exception handling
- Log errors with appropriate context
- Provide clear error messages
- Include recovery steps where possible

### 4. Testing
- Write unit tests for new functionality
- Test edge cases and error conditions
- Maintain 80% code coverage
- Test agent and task distribution logic

### 5. Documentation
- Add docstrings to all functions and classes
- Keep README.md up to date
- Document configuration changes
- Include usage examples

### 6. Performance
- Monitor task execution
- Log progress and intermediate results
- Save state for long-running operations
- Consider memory usage with large agent pools

### 7. Configuration
- Use YAML for configuration files
- Validate all configuration parameters
- Document configuration options
- Keep backwards compatibility

## Pull Request Process
1. Update documentation
2. Add/update tests
3. Follow code standards
4. Update CHANGELOG.md
5. Request review
