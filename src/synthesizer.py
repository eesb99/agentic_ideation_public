"""
Synthesizer module for combining and analyzing results.
"""
from typing import Dict, Any, List
from utils import make_api_call, log_message, save_to_yaml
from datetime import datetime, timedelta
import os

def create_synthesizer_agent(topic: str) -> Dict[str, Any]:
    """Create a synthesizer agent."""
    return {
        "name": "Synthesizer Agent",
        "persona": f"You are a synthesizer specializing in summarizing all subtasks related to {topic}.",
        "model": "deepseek/deepseek-chat"
    }

def chunk_hierarchical_results(results: Dict) -> List[Dict]:
    """
    Break down hierarchical results into manageable chunks.
    Returns a list of smaller result dictionaries.
    """
    chunks = []
    current_chunk = {}
    current_size = 0
    max_size = 8000  # Reduced to 8K tokens to allow for synthesis overhead
    
    for level_name, level_tasks in results.items():
        for focus, focus_tasks in level_tasks.items():
            # Estimate size of current focus group
            focus_size = sum(len(str(task)) for task in focus_tasks.values())
            
            if current_size + focus_size > max_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = {}
                current_size = 0
            
            if focus_size > max_size:
                # Split large focus groups into smaller chunks
                temp_tasks = {}
                temp_size = 0
                for task_id, task_result in focus_tasks.items():
                    task_size = len(str(task_result))
                    if temp_size + task_size > max_size:
                        if temp_tasks:
                            chunks.append({level_name: {focus: temp_tasks}})
                            temp_tasks = {}
                            temp_size = 0
                    # Truncate very long results
                    truncated_result = str(task_result)[:1500] + "..." if len(str(task_result)) > 1500 else str(task_result)
                    temp_tasks[task_id] = truncated_result
                    temp_size += len(truncated_result)
                if temp_tasks:
                    chunks.append({level_name: {focus: temp_tasks}})
            else:
                if level_name not in current_chunk:
                    current_chunk[level_name] = {}
                current_chunk[level_name][focus] = {
                    task_id: str(result)[:1500] + "..." if len(str(result)) > 1500 else str(result)
                    for task_id, result in focus_tasks.items()
                }
                current_size += focus_size
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

async def summarize_results(results: Dict, synthesizer_agent: Dict, topic: str, synthesizer_prompt: str) -> str:
    """
    Summarize results using a hierarchical, chunked approach to handle token limits.
    """
    try:
        if not results:
            log_message("No results to summarize", "error")
            return None
            
        start_time = datetime.now()
        log_message("Starting results summarization", "info")
        
        # Stage 1: Split results into manageable chunks
        try:
            chunks = chunk_hierarchical_results(results)
            chunk_count = len(chunks)
            log_message(f"Split results into {chunk_count} manageable chunks", "info")
            if chunk_count == 0:
                log_message("No chunks generated from results", "error")
                return None
        except Exception as e:
            log_message(f"Error splitting results into chunks: {str(e)}", "error")
            return None
        
        # Stage 2: Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            log_message(f"Processing chunk {i}/{chunk_count}", "info")
            
            try:
                # Format chunk with hierarchical structure
                chunk_text = format_chunk_text(chunk)
                if not chunk_text:
                    log_message(f"Empty chunk text for chunk {i}", "warning")
                    continue
                    
                chunk_prompt = create_chunk_prompt(chunk_text, topic)
                response = await make_api_call(
                    [{"role": "user", "content": chunk_prompt}],
                    synthesizer_agent["model"],
                    f"Summarizing chunk {i}"
                )
                
                if response:
                    chunk_summaries.append(response)
                    log_message(f"Successfully summarized chunk {i}", "success")
                else:
                    log_message(f"Failed to get response for chunk {i}", "error")
            
            except Exception as e:
                log_message(f"Error processing chunk {i}: {str(e)}", "error")
                continue
        
        # Stage 3: Final synthesis of chunk summaries
        if not chunk_summaries:
            log_message("No successful chunk summaries generated", "error")
            return None
            
        try:
            end_time = datetime.now()
            processing_duration = end_time - start_time
            
            timestamp_info = create_timestamp_info(end_time, processing_duration, chunk_count)
            final_prompt = create_final_prompt(topic, chunk_summaries)
            
            final_summary = await make_api_call(
                [{"role": "user", "content": final_prompt}],
                synthesizer_agent["model"],
                "Creating final synthesis"
            )
            
            if final_summary:
                log_message("Successfully generated final synthesis", "success")
                return format_final_summary(final_summary, timestamp_info, topic, end_time)
            else:
                log_message("Failed to generate final synthesis", "error")
                return None
                
        except Exception as e:
            log_message(f"Error in final synthesis: {str(e)}", "error")
            return None
            
    except Exception as e:
        log_message(f"Critical error in summarization: {str(e)}", "error")
        return None

def format_chunk_text(chunk: Dict) -> str:
    """Format chunk into readable text."""
    chunk_text = ""
    try:
        for level_name, level_tasks in chunk.items():
            chunk_text += f"\n\nLevel: {level_name}\n"
            for focus, focus_tasks in level_tasks.items():
                chunk_text += f"\nFocus Area: {focus}\n"
                for task_id, task_result in focus_tasks.items():
                    # Ensure task_result is a string and limit its length
                    result_text = str(task_result)[:2000] + "..." if len(str(task_result)) > 2000 else str(task_result)
                    chunk_text += f"\n{task_id}: {result_text}"
        return chunk_text
    except Exception as e:
        log_message(f"Error formatting chunk text: {str(e)}", "error")
        return ""

def create_chunk_prompt(chunk_text: str, topic: str) -> str:
    """Create the prompt for summarizing a chunk."""
    return (
        f"Summarize this chunk of results for topic: {topic}\n"
        f"Focus on key insights while maintaining the hierarchical structure.\n"
        f"Format your response with clear sections and avoid repetition.\n\n"
        f"{chunk_text}"
    )

def create_timestamp_info(end_time: datetime, duration: timedelta, chunk_count: int) -> str:
    """Create formatted timestamp information."""
    return (
        f"Analysis Timestamp: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Processing Duration: {duration}\n"
        f"Total Chunks Processed: {chunk_count}\n"
        f"{'='*50}\n\n"
    )

def create_final_prompt(topic: str, summaries: List[str]) -> str:
    """Create the prompt for final synthesis."""
    return (
        f"Create a final synthesis for topic: {topic}\n"
        f"Combine these summaries into a cohesive analysis.\n"
        f"Format your response with these sections:\n"
        f"1. Executive Summary\n"
        f"2. Key Findings\n"
        f"3. Critical Insights\n"
        f"4. Recommendations\n"
        f"5. Conclusion (single, concise paragraph)\n\n"
        + "\n\n---\n\n".join(summaries)
    )

def format_final_summary(summary: str, timestamp_info: str, topic: str, end_time: datetime) -> str:
    """Format the final summary with metadata."""
    return (
        f"=== Final Analysis ===\n"
        f"{timestamp_info}"
        f"Topic: {topic}\n\n"
        f"{summary}\n\n"
        f"{'='*50}\n"
        f"End of Analysis - Generated at {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )

async def deploy_deep_dive_agents(key_areas: str, results: Dict, config: Dict, synthesizer_agent: Dict) -> List[Dict]:
    """
    Deploy specialized agents for deep dive analysis.
    """
    deep_dive_findings = []
    
    if not config.deep_dive_agents:
        log_message("No deep dive agents configured", "warning")
        return []
        
    for agent_type in config.deep_dive_agents[0].agent_types:
        log_message(f"Deploying {agent_type.name} agents...", "info")
        
        analysis_prompt = (
            f"As a {agent_type.name}, your focus is to {agent_type.focus}.\n"
            f"Analyze these key areas:\n{key_areas}\n\n"
            f"Consider:\n"
            f"1. Specific insights within your focus area\n"
            f"2. Cross-domain implications\n"
            f"3. Actionable recommendations\n"
            f"4. Critical dependencies\n"
            f"5. Success metrics\n\n"
        )
        
        # Deploy multiple agents of this type
        agent_findings = []
        for i in range(agent_type.num_agents):
            agent_response = await make_api_call(
                [{"role": "user", "content": analysis_prompt}],
                synthesizer_agent["model"],
                f"Agent {i+1} of {agent_type.name}"
            )
            if agent_response:
                agent_findings.append(agent_response)
        
        if agent_findings:
            # Synthesize findings from all agents of this type
            synthesis_prompt = (
                f"Synthesize these {agent_type.name} findings into cohesive insights:\n\n" +
                "\n---\n".join(agent_findings)
            )
            
            type_synthesis = await make_api_call(
                [{"role": "user", "content": synthesis_prompt}],
                synthesizer_agent["model"],
                f"Synthesizing {agent_type.name} findings"
            )
            
            if type_synthesis:
                deep_dive_findings.append({
                    "agent_type": agent_type.name,
                    "focus": agent_type.focus,
                    "synthesis": type_synthesis
                })
    
    return deep_dive_findings

async def deep_dive_analysis(initial_summary: str, results: Dict, config: Dict, topic: str, synthesizer_agent: Dict) -> str:
    """
    Perform a deep dive analysis using specialized agents.
    """
    try:
        start_time = datetime.now()
        log_message("Starting deep dive analysis with specialized agents...", "info")
        
        # Extract key areas for deep dive from initial summary
        deep_dive_prompt = (
            f"Analyze this initial summary and identify 5 key areas that warrant deeper investigation:\n\n{initial_summary}"
        )
        
        key_areas_response = await make_api_call(
            [{"role": "user", "content": deep_dive_prompt}],
            synthesizer_agent["model"],
            "Identifying key areas for deep dive"
        )
        
        if not key_areas_response:
            return None
        
        # Deploy specialized agents for deep dive analysis
        deep_dive_findings = await deploy_deep_dive_agents(key_areas_response, results, config, synthesizer_agent)
        
        # Synthesize all deep dive findings
        if deep_dive_findings:
            end_time = datetime.now()
            timestamp_info = (
                f"Deep Dive Analysis Timestamp: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Analysis Duration: {end_time - start_time}\n"
                f"Specialized Agent Types: {len(deep_dive_findings)}\n"
                f"{'='*50}\n\n"
            )
            
            final_synthesis = (
                f"=== Deep Dive Analysis ===\n"
                f"{timestamp_info}"
                f"Topic: {topic}\n\n"
                f"Key Areas Investigated:\n{key_areas_response}\n\n"
                f"=== Specialized Agent Findings ===\n\n"
            )
            
            for finding in deep_dive_findings:
                final_synthesis += (
                    f"\n{finding['agent_type']} Insights\n"
                    f"Focus: {finding['focus']}\n"
                    f"{finding['synthesis']}\n"
                    f"{'-'*50}\n"
                )
            
            final_synthesis += (
                f"\n{'='*50}\n"
                f"End of Deep Dive - Generated at {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            return final_synthesis
        
        return None
    except Exception as e:
        log_message(f"Error in deep dive analysis: {str(e)}", "error")
        return None

async def analyze_results(results: Dict, config: Dict, topic: str, synthesizer_prompt: str) -> Dict[str, str]:
    """
    Perform complete analysis including initial summary and deep dive.
    """
    try:
        # Get initial summary
        synthesizer_agent = create_synthesizer_agent(topic)
        initial_summary = await summarize_results(results, synthesizer_agent, topic, synthesizer_prompt)
        if not initial_summary:
            log_message("Failed to generate initial summary", "error")
            return {
                "initial_summary": "Summary generation failed",
                "deep_dive_analysis": "Analysis not available due to summary failure"
            }
        
        # Perform deep dive analysis
        try:
            deep_dive = await deep_dive_analysis(initial_summary, results, config, topic, synthesizer_agent)
        except Exception as e:
            log_message(f"Error in deep dive analysis: {str(e)}", "error")
            deep_dive = None
        
        return {
            "initial_summary": initial_summary,
            "deep_dive_analysis": deep_dive if deep_dive else "Deep dive analysis not available"
        }
    except Exception as e:
        log_message(f"Error in analysis: {str(e)}", "error")
        return {
            "initial_summary": f"Analysis failed: {str(e)}",
            "deep_dive_analysis": "Analysis not available due to error"
        }
