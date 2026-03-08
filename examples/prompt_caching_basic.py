"""
Basic Prompt Caching Example with Claude
Demonstrates how to cache system prompts for cost savings
"""

import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Example 1: Without Caching (Expensive)
def without_caching():
    """Traditional approach - pay full price every time"""
    
    system_prompt = """You are a Senior Product Manager with 10+ years of experience 
    in software development. You excel at understanding user needs, defining clear 
    requirements, and creating detailed product requirement documents (PRD). 
    You think about user stories, acceptance criteria, and success metrics. 
    You ensure all stakeholders understand what needs to be built."""
    
    # Call 1
    response1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,  # 500 tokens - full price
        messages=[
            {"role": "user", "content": "Create a PRD for a todo app"}
        ]
    )
    print("Call 1 cost: ~$0.0015 (system) + output")
    
    # Call 2 - Same system prompt, different request
    response2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,  # 500 tokens - full price AGAIN!
        messages=[
            {"role": "user", "content": "Create a PRD for a blog API"}
        ]
    )
    print("Call 2 cost: ~$0.0015 (system) + output")
    print("Total system prompt cost: ~$0.003")


# Example 2: With Caching (90% Cheaper)
def with_caching():
    """Optimized approach - cache the system prompt"""
    
    system_prompt = """You are a Senior Product Manager with 10+ years of experience 
    in software development. You excel at understanding user needs, defining clear 
    requirements, and creating detailed product requirement documents (PRD). 
    You think about user stories, acceptance criteria, and success metrics. 
    You ensure all stakeholders understand what needs to be built."""
    
    # Call 1 - Write to cache
    response1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}  # 🔑 Cache this!
            }
        ],
        messages=[
            {"role": "user", "content": "Create a PRD for a todo app"}
        ]
    )
    print("Call 1 cost: ~$0.00188 (cache write) + output")
    
    # Call 2 - Read from cache (within 5 minutes)
    response2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": system_prompt,  # Same prompt
                "cache_control": {"type": "ephemeral"}  # Cache hit!
            }
        ],
        messages=[
            {"role": "user", "content": "Create a PRD for a blog API"}
        ]
    )
    print("Call 2 cost: ~$0.00015 (cache read - 90% off!) + output")
    print("Total system prompt cost: ~$0.002 (33% savings)")
    
    # Call 3, 4, 5... within 5 minutes
    # Each costs only $0.00015 for the system prompt!


# Example 3: Check Cache Usage
def check_cache_usage():
    """See how much you're saving with caching"""
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a helpful assistant.",
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # Check usage statistics
    usage = response.usage
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Cache creation tokens: {usage.cache_creation_input_tokens}")
    print(f"Cache read tokens: {usage.cache_read_input_tokens}")
    print(f"Output tokens: {usage.output_tokens}")
    
    # Calculate cost
    cache_write_cost = usage.cache_creation_input_tokens * 3.75 / 1_000_000
    cache_read_cost = usage.cache_read_input_tokens * 0.30 / 1_000_000
    input_cost = usage.input_tokens * 3.00 / 1_000_000
    output_cost = usage.output_tokens * 15.00 / 1_000_000
    
    total_cost = cache_write_cost + cache_read_cost + input_cost + output_cost
    print(f"\nTotal cost: ${total_cost:.6f}")


if __name__ == "__main__":
    print("=== Without Caching ===")
    without_caching()
    
    print("\n=== With Caching ===")
    with_caching()
    
    print("\n=== Check Cache Usage ===")
    check_cache_usage()
