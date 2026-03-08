"""
Interactive Cost Calculator for Prompt Caching
Shows real-time cost comparison for your specific use case
"""


def calculate_costs(num_projects, system_tokens, context_tokens, message_tokens, output_tokens):
    """
    Calculate costs with and without caching
    
    Args:
        num_projects: Number of projects to process
        system_tokens: Size of system prompt (agent instructions)
        context_tokens: Size of context (previous outputs, docs)
        message_tokens: Size of user message
        output_tokens: Expected output size
    
    Returns:
        dict with cost breakdown
    """
    # Pricing (per 1M tokens)
    REGULAR_INPUT = 3.00
    CACHE_WRITE = 3.75
    CACHE_READ = 0.30
    OUTPUT = 15.00
    
    # Without caching
    input_per_call = (system_tokens + context_tokens + message_tokens) * REGULAR_INPUT / 1_000_000
    output_per_call = output_tokens * OUTPUT / 1_000_000
    cost_per_call_no_cache = input_per_call + output_per_call
    total_no_cache = cost_per_call_no_cache * num_projects
    
    # With caching
    # First call: cache write
    first_call_input = (
        (system_tokens + context_tokens) * CACHE_WRITE / 1_000_000 +
        message_tokens * REGULAR_INPUT / 1_000_000
    )
    first_call_output = output_tokens * OUTPUT / 1_000_000
    first_call_cost = first_call_input + first_call_output
    
    # Subsequent calls: cache read
    subsequent_input = (
        (system_tokens + context_tokens) * CACHE_READ / 1_000_000 +
        message_tokens * REGULAR_INPUT / 1_000_000
    )
    subsequent_output = output_tokens * OUTPUT / 1_000_000
    subsequent_cost = subsequent_input + subsequent_output
    
    total_with_cache = first_call_cost + (subsequent_cost * (num_projects - 1))
    
    # Savings
    savings = total_no_cache - total_with_cache
    savings_percent = (savings / total_no_cache * 100) if total_no_cache > 0 else 0
    
    return {
        "without_cache": {
            "per_call": cost_per_call_no_cache,
            "total": total_no_cache
        },
        "with_cache": {
            "first_call": first_call_cost,
            "subsequent_call": subsequent_cost,
            "total": total_with_cache
        },
        "savings": {
            "amount": savings,
            "percent": savings_percent
        }
    }


def print_cost_breakdown(results, num_projects):
    """Pretty print the cost breakdown"""
    print("\n" + "="*70)
    print("COST BREAKDOWN")
    print("="*70)
    
    print(f"\n📊 Scenario: {num_projects} projects")
    
    print("\n--- WITHOUT CACHING ---")
    print(f"Cost per project: ${results['without_cache']['per_call']:.6f}")
    print(f"Total cost: ${results['without_cache']['total']:.4f}")
    
    print("\n--- WITH CACHING ---")
    print(f"First project (cache write): ${results['with_cache']['first_call']:.6f}")
    print(f"Subsequent projects (cache read): ${results['with_cache']['subsequent_call']:.6f}")
    print(f"Total cost: ${results['with_cache']['total']:.4f}")
    
    print("\n--- SAVINGS ---")
    print(f"💰 Amount saved: ${results['savings']['amount']:.4f}")
    print(f"📈 Percentage saved: {results['savings']['percent']:.1f}%")
    
    # ROI timeline
    print("\n--- SAVINGS OVER TIME ---")
    for multiplier, period in [(1, "month"), (12, "year"), (36, "3 years")]:
        total_savings = results['savings']['amount'] * multiplier
        print(f"Per {period}: ${total_savings:.2f}")


def interactive_calculator():
    """Interactive cost calculator"""
    print("\n" + "="*70)
    print("PROMPT CACHING COST CALCULATOR")
    print("="*70)
    print("\nThis calculator shows how much you can save with prompt caching.")
    print("Answer a few questions about your use case:\n")
    
    # Get user input
    try:
        num_projects = int(input("How many projects per month? (e.g., 100): "))
        
        print("\n--- Token Estimates ---")
        print("Tip: 1 token ≈ 4 characters or 0.75 words")
        print("Example system prompt (500 words) ≈ 650 tokens")
        
        system_tokens = int(input("\nSystem prompt size in tokens? (e.g., 500): "))
        context_tokens = int(input("Context size in tokens? (e.g., 2000): "))
        message_tokens = int(input("User message size in tokens? (e.g., 100): "))
        output_tokens = int(input("Expected output size in tokens? (e.g., 2000): "))
        
        # Calculate
        results = calculate_costs(
            num_projects,
            system_tokens,
            context_tokens,
            message_tokens,
            output_tokens
        )
        
        # Display results
        print_cost_breakdown(results, num_projects)
        
        # Additional insights
        print("\n" + "="*70)
        print("INSIGHTS")
        print("="*70)
        
        cacheable_tokens = system_tokens + context_tokens
        cacheable_percent = (cacheable_tokens / (system_tokens + context_tokens + message_tokens)) * 100
        
        print(f"\n✓ Cacheable content: {cacheable_tokens:,} tokens ({cacheable_percent:.0f}%)")
        print(f"✓ Break-even point: 2 projects")
        print(f"✓ Cache duration: 5 minutes")
        
        if results['savings']['percent'] > 50:
            print(f"\n🎉 Excellent! You'll save {results['savings']['percent']:.0f}% with caching!")
        elif results['savings']['percent'] > 25:
            print(f"\n👍 Good! You'll save {results['savings']['percent']:.0f}% with caching.")
        else:
            print(f"\n💡 Moderate savings of {results['savings']['percent']:.0f}%. Consider increasing cacheable content.")
        
    except ValueError:
        print("\n❌ Invalid input. Please enter numbers only.")
    except KeyboardInterrupt:
        print("\n\nCalculator closed.")


def preset_scenarios():
    """Show preset scenarios for common use cases"""
    print("\n" + "="*70)
    print("PRESET SCENARIOS")
    print("="*70)
    
    scenarios = [
        {
            "name": "Small Dev Team (Light Usage)",
            "projects": 50,
            "system": 500,
            "context": 1000,
            "message": 100,
            "output": 1500
        },
        {
            "name": "Medium Dev Team (Moderate Usage)",
            "projects": 200,
            "system": 800,
            "context": 3000,
            "message": 150,
            "output": 2500
        },
        {
            "name": "Large Dev Team (Heavy Usage)",
            "projects": 1000,
            "system": 1000,
            "context": 5000,
            "message": 200,
            "output": 3000
        },
        {
            "name": "Enterprise (Very Heavy Usage)",
            "projects": 5000,
            "system": 1500,
            "context": 8000,
            "message": 250,
            "output": 4000
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*70}")
        print(f"Scenario {i}: {scenario['name']}")
        print(f"{'='*70}")
        
        results = calculate_costs(
            scenario['projects'],
            scenario['system'],
            scenario['context'],
            scenario['message'],
            scenario['output']
        )
        
        print(f"\nProjects per month: {scenario['projects']}")
        print(f"System prompt: {scenario['system']} tokens")
        print(f"Context: {scenario['context']} tokens")
        print(f"Message: {scenario['message']} tokens")
        print(f"Output: {scenario['output']} tokens")
        
        print(f"\n💰 Without caching: ${results['without_cache']['total']:.2f}/month")
        print(f"💰 With caching: ${results['with_cache']['total']:.2f}/month")
        print(f"✅ Savings: ${results['savings']['amount']:.2f}/month ({results['savings']['percent']:.1f}%)")
        print(f"📅 Annual savings: ${results['savings']['amount'] * 12:.2f}")


def main():
    """Main menu"""
    while True:
        print("\n" + "="*70)
        print("PROMPT CACHING COST CALCULATOR")
        print("="*70)
        print("\nChoose an option:")
        print("1. Interactive calculator (custom values)")
        print("2. View preset scenarios")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            interactive_calculator()
        elif choice == "2":
            preset_scenarios()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
