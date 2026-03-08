"""
Advanced Prompt Caching Examples
Shows real-world use cases for the Software Development Team
"""

import anthropic
import os
from datetime import datetime

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Use Case 1: Cache Agent System Prompts
def cache_agent_prompts():
    """Cache system prompts for each agent in your dev team"""
    
    # Product Manager agent with cached system prompt
    pm_system_prompt = """You are an experienced Product Manager with 10+ years 
    in software development. You excel at understanding user needs, defining clear 
    requirements, and creating detailed product requirement documents (PRD). 
    You think about user stories, acceptance criteria, and success metrics."""
    
    # Process 10 different projects
    projects = [
        "Build a REST API for a blog",
        "Create a todo list application",
        "Design a user authentication system",
        "Build an e-commerce platform",
        "Create a real-time chat application"
    ]
    
    total_cost = 0
    
    for i, project in enumerate(projects):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": pm_system_prompt,
                    "cache_control": {"type": "ephemeral"}  # Cache this
                }
            ],
            messages=[
                {"role": "user", "content": f"Create a PRD for: {project}"}
            ]
        )
        
        # Calculate cost for this call
        usage = response.usage
        if i == 0:
            # First call - cache write
            cost = (usage.cache_creation_input_tokens * 3.75 / 1_000_000 +
                   usage.output_tokens * 15.00 / 1_000_000)
            print(f"Project {i+1}: Cache WRITE - ${cost:.6f}")
        else:
            # Subsequent calls - cache read (90% off!)
            cost = (usage.cache_read_input_tokens * 0.30 / 1_000_000 +
                   usage.input_tokens * 3.00 / 1_000_000 +
                   usage.output_tokens * 15.00 / 1_000_000)
            print(f"Project {i+1}: Cache READ - ${cost:.6f}")
        
        total_cost += cost
    
    print(f"\nTotal cost for 5 projects: ${total_cost:.6f}")
    print(f"Without caching would be: ~${total_cost * 2:.6f}")
    print(f"Savings: ~${total_cost:.6f} (50%)")


# Use Case 2: Cache Context from Previous Agents
def cache_previous_agent_outputs():
    """Cache outputs from previous agents as context for next agents"""
    
    # Step 1: PM creates PRD
    pm_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=[{
            "type": "text",
            "text": "You are a Product Manager. Create detailed PRDs.",
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[
            {"role": "user", "content": "Create a PRD for a blog API"}
        ]
    )
    
    prd = pm_response.content[0].text
    print(f"PM created PRD ({len(prd)} chars)")
    
    # Step 2: Architect uses PRD (cached as context)
    architect_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": "You are a Software Architect. Design systems based on PRDs.",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Product Requirements Document:\n\n{prd}",
                "cache_control": {"type": "ephemeral"}  # Cache the PRD too!
            }
        ],
        messages=[
            {"role": "user", "content": "Design the system architecture"}
        ]
    )
    
    architecture = architect_response.content[0].text
    print(f"Architect created design ({len(architecture)} chars)")
    
    # Step 3: Developer uses PRD + Architecture (both cached!)
    developer_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": "You are a Senior Developer. Write production-ready code.",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Product Requirements:\n\n{prd}",
                "cache_control": {"type": "ephemeral"}  # Cached from before!
            },
            {
                "type": "text",
                "text": f"Architecture Design:\n\n{architecture}",
                "cache_control": {"type": "ephemeral"}  # Cache this too
            }
        ],
        messages=[
            {"role": "user", "content": "Implement the blog API"}
        ]
    )
    
    print(f"Developer wrote code ({len(developer_response.content[0].text)} chars)")
    print("\n💡 PRD was cached and reused - saved 90% on those tokens!")


# Use Case 3: Cache Large Documentation
def cache_large_documentation():
    """Cache large codebases or documentation for reference"""
    
    # Simulate a large codebase or API documentation
    large_documentation = """
    # API Documentation (10,000+ tokens)
    
    ## Authentication Endpoints
    POST /api/auth/login
    POST /api/auth/register
    POST /api/auth/logout
    
    ## Blog Post Endpoints
    GET /api/posts - List all posts
    GET /api/posts/:id - Get single post
    POST /api/posts - Create post
    PUT /api/posts/:id - Update post
    DELETE /api/posts/:id - Delete post
    
    ## Comment Endpoints
    GET /api/posts/:id/comments - List comments
    POST /api/posts/:id/comments - Create comment
    
    [... imagine 10,000 more tokens of documentation ...]
    """ * 50  # Simulate large doc
    
    # Multiple queries against the same documentation
    queries = [
        "How do I authenticate users?",
        "Show me the blog post endpoints",
        "How do I create a comment?",
        "What's the rate limiting policy?",
        "How do I handle errors?"
    ]
    
    for i, query in enumerate(queries):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": "You are a helpful API documentation assistant.",
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": large_documentation,
                    "cache_control": {"type": "ephemeral"}  # Cache the docs!
                }
            ],
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        usage = response.usage
        if i == 0:
            print(f"Query {i+1}: Cached {usage.cache_creation_input_tokens} tokens")
        else:
            print(f"Query {i+1}: Read {usage.cache_read_input_tokens} cached tokens (90% off!)")


# Use Case 4: Multi-turn Conversations with Caching
def cache_conversation_history():
    """Cache conversation history for multi-turn interactions"""
    
    system_prompt = "You are a helpful coding assistant."
    conversation_history = []
    
    # Turn 1
    response1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[
            {"role": "user", "content": "Write a Python function to reverse a string"}
        ]
    )
    
    conversation_history.append({
        "role": "user",
        "content": "Write a Python function to reverse a string"
    })
    conversation_history.append({
        "role": "assistant",
        "content": response1.content[0].text
    })
    
    # Turn 2 - Cache the conversation history
    response2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=conversation_history + [
            {
                "role": "user",
                "content": "Now add error handling",
                "cache_control": {"type": "ephemeral"}  # Cache history
            }
        ]
    )
    
    print("Turn 1: Created cache")
    print("Turn 2: Used cached conversation (90% off on history!)")


# Use Case 5: Cost Comparison Dashboard
def cost_comparison():
    """Show real cost savings with caching"""
    
    print("\n" + "="*60)
    print("COST COMPARISON: With vs Without Caching")
    print("="*60)
    
    # Scenario: 100 API calls with same system prompt (500 tokens)
    system_tokens = 500
    message_tokens = 100
    output_tokens = 1000
    num_calls = 100
    
    # Without caching
    without_cache_cost = (
        (system_tokens + message_tokens) * num_calls * 3.00 / 1_000_000 +
        output_tokens * num_calls * 15.00 / 1_000_000
    )
    
    # With caching
    first_call_cost = (
        system_tokens * 3.75 / 1_000_000 +  # Cache write
        message_tokens * 3.00 / 1_000_000 +
        output_tokens * 15.00 / 1_000_000
    )
    
    subsequent_call_cost = (
        system_tokens * 0.30 / 1_000_000 +  # Cache read (90% off!)
        message_tokens * 3.00 / 1_000_000 +
        output_tokens * 15.00 / 1_000_000
    )
    
    with_cache_cost = first_call_cost + (subsequent_call_cost * 99)
    
    print(f"\nScenario: 100 API calls")
    print(f"System prompt: {system_tokens} tokens")
    print(f"Message: {message_tokens} tokens")
    print(f"Output: {output_tokens} tokens")
    print(f"\nWithout caching: ${without_cache_cost:.4f}")
    print(f"With caching: ${with_cache_cost:.4f}")
    print(f"Savings: ${without_cache_cost - with_cache_cost:.4f} ({((without_cache_cost - with_cache_cost) / without_cache_cost * 100):.1f}%)")
    
    # Scale up
    print(f"\n--- Scaled to 1,000 calls ---")
    print(f"Without caching: ${without_cache_cost * 10:.2f}")
    print(f"With caching: ${with_cache_cost * 10:.2f}")
    print(f"Savings: ${(without_cache_cost - with_cache_cost) * 10:.2f}")
    
    print(f"\n--- Scaled to 10,000 calls ---")
    print(f"Without caching: ${without_cache_cost * 100:.2f}")
    print(f"With caching: ${with_cache_cost * 100:.2f}")
    print(f"Savings: ${(without_cache_cost - with_cache_cost) * 100:.2f}")


if __name__ == "__main__":
    print("Choose an example:")
    print("1. Cache agent system prompts")
    print("2. Cache previous agent outputs")
    print("3. Cache large documentation")
    print("4. Cache conversation history")
    print("5. Cost comparison")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == "1":
        cache_agent_prompts()
    elif choice == "2":
        cache_previous_agent_outputs()
    elif choice == "3":
        cache_large_documentation()
    elif choice == "4":
        cache_conversation_history()
    elif choice == "5":
        cost_comparison()
    else:
        print("Invalid choice")
