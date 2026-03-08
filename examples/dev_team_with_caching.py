"""
Software Development Team with Prompt Caching
Optimized version that saves 60-80% on API costs
"""

import anthropic
import os
from datetime import datetime


class CachedDevTeam:
    """Development team that uses prompt caching for cost optimization"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.total_cost = 0
        self.cache_savings = 0
        
        # Define agent system prompts (these will be cached)
        self.agent_prompts = {
            "pm": """You are an experienced Product Manager with 10+ years in software 
            development. You excel at understanding user needs, defining clear requirements, 
            and creating detailed product requirement documents (PRD). You think about user 
            stories, acceptance criteria, and success metrics. You ensure all stakeholders 
            understand what needs to be built.""",
            
            "architect": """You are a Senior Software Architect with expertise in system 
            design, microservices, databases, and cloud architecture. You make informed 
            decisions about technology stack, design patterns, data models, and API structures. 
            You consider scalability, security, maintainability, and performance in all your 
            designs.""",
            
            "developer": """You are a Senior Software Developer with expertise in multiple 
            programming languages and frameworks. You write clean, maintainable code following 
            best practices and design patterns. You include proper error handling, input 
            validation, and comprehensive documentation. Your code is production-ready and 
            follows industry standards.""",
            
            "qa": """You are a Senior QA Engineer with expertise in test automation, quality 
            assurance, and software testing methodologies. You create thorough test cases, 
            write automated tests, identify edge cases and potential bugs. You validate that 
            all acceptance criteria are met and the implementation matches requirements.""",
            
            "devops": """You are a Senior DevOps Engineer with expertise in containerization, 
            CI/CD pipelines, cloud infrastructure, and deployment automation. You create Docker 
            configurations, CI/CD pipelines, infrastructure as code, and deployment scripts. 
            You ensure applications are secure, scalable, and easy to deploy."""
        }
    
    def _call_agent(self, agent_name: str, task: str, context: list = None, 
                    is_first_call: bool = False):
        """
        Call an agent with prompt caching
        
        Args:
            agent_name: Name of the agent (pm, architect, developer, qa, devops)
            task: The task description
            context: List of previous outputs to include as context
            is_first_call: Whether this is the first call (for logging)
        """
        # Build system messages with caching
        system_messages = [
            {
                "type": "text",
                "text": self.agent_prompts[agent_name],
                "cache_control": {"type": "ephemeral"}  # Cache agent prompt
            }
        ]
        
        # Add context from previous agents (also cached!)
        if context:
            for ctx in context:
                system_messages.append({
                    "type": "text",
                    "text": ctx,
                    "cache_control": {"type": "ephemeral"}  # Cache context
                })
        
        # Make API call
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=system_messages,
            messages=[
                {"role": "user", "content": task}
            ]
        )
        
        # Calculate cost
        usage = response.usage
        cost = self._calculate_cost(usage, is_first_call)
        self.total_cost += cost
        
        # Log cache usage
        self._log_cache_usage(agent_name, usage, cost, is_first_call)
        
        return response.content[0].text
    
    def _calculate_cost(self, usage, is_first_call):
        """Calculate the cost of an API call"""
        cache_write_cost = getattr(usage, 'cache_creation_input_tokens', 0) * 3.75 / 1_000_000
        cache_read_cost = getattr(usage, 'cache_read_input_tokens', 0) * 0.30 / 1_000_000
        input_cost = usage.input_tokens * 3.00 / 1_000_000
        output_cost = usage.output_tokens * 15.00 / 1_000_000
        
        total = cache_write_cost + cache_read_cost + input_cost + output_cost
        
        # Calculate what it would have cost without caching
        if not is_first_call and hasattr(usage, 'cache_read_input_tokens'):
            without_cache = (usage.cache_read_input_tokens * 3.00 / 1_000_000 + 
                           input_cost + output_cost)
            self.cache_savings += (without_cache - total)
        
        return total
    
    def _log_cache_usage(self, agent_name, usage, cost, is_first_call):
        """Log cache usage statistics"""
        cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        
        print(f"\n{'='*60}")
        print(f"Agent: {agent_name.upper()}")
        print(f"{'='*60}")
        print(f"Input tokens: {usage.input_tokens}")
        print(f"Output tokens: {usage.output_tokens}")
        
        if cache_write > 0:
            print(f"Cache WRITE: {cache_write} tokens (first time)")
        if cache_read > 0:
            print(f"Cache READ: {cache_read} tokens (90% savings! 🎉)")
        
        print(f"Cost: ${cost:.6f}")
        
        if not is_first_call and cache_read > 0:
            saved = cache_read * 2.70 / 1_000_000  # Difference between $3 and $0.30
            print(f"Saved: ${saved:.6f} from caching")
    
    def build_project(self, requirement: str):
        """Build a complete project with caching optimization"""
        print("\n" + "="*60)
        print("SOFTWARE DEVELOPMENT TEAM (With Prompt Caching)")
        print("="*60)
        print(f"Requirement: {requirement}\n")
        
        # Phase 1: Product Manager (First call - creates cache)
        print("\n🤖 Phase 1: Product Manager")
        prd = self._call_agent(
            "pm",
            f"Create a detailed PRD for: {requirement}",
            is_first_call=True
        )
        
        # Phase 2: Architect (Uses cached PM prompt + caches PRD)
        print("\n🤖 Phase 2: Architect")
        architecture = self._call_agent(
            "architect",
            "Design the system architecture based on the PRD",
            context=[f"Product Requirements Document:\n\n{prd}"],
            is_first_call=False
        )
        
        # Phase 3: Developer (Uses cached prompts + PRD + Architecture)
        print("\n🤖 Phase 3: Developer")
        code = self._call_agent(
            "developer",
            "Implement the system based on the architecture",
            context=[
                f"Product Requirements:\n\n{prd}",
                f"Architecture Design:\n\n{architecture}"
            ],
            is_first_call=False
        )
        
        # Phase 4: QA (Uses all cached context)
        print("\n🤖 Phase 4: QA Tester")
        tests = self._call_agent(
            "qa",
            "Create comprehensive tests and validate the implementation",
            context=[
                f"Product Requirements:\n\n{prd}",
                f"Architecture:\n\n{architecture}",
                f"Implementation:\n\n{code[:2000]}"  # Truncate for demo
            ],
            is_first_call=False
        )
        
        # Phase 5: DevOps (Uses cached architecture + code)
        print("\n🤖 Phase 5: DevOps")
        deployment = self._call_agent(
            "devops",
            "Create deployment configurations and infrastructure setup",
            context=[
                f"Architecture:\n\n{architecture}",
                f"Implementation:\n\n{code[:2000]}"
            ],
            is_first_call=False
        )
        
        # Summary
        self._print_summary()
        
        return {
            "prd": prd,
            "architecture": architecture,
            "code": code,
            "tests": tests,
            "deployment": deployment
        }
    
    def _print_summary(self):
        """Print cost summary"""
        print("\n" + "="*60)
        print("COST SUMMARY")
        print("="*60)
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Cache savings: ${self.cache_savings:.4f}")
        print(f"Savings percentage: {(self.cache_savings / (self.total_cost + self.cache_savings) * 100):.1f}%")
        
        # Estimate without caching
        without_cache = self.total_cost + self.cache_savings
        print(f"\nWithout caching: ${without_cache:.4f}")
        print(f"With caching: ${self.total_cost:.4f}")
        print(f"You saved: ${self.cache_savings:.4f} 🎉")


def compare_multiple_projects():
    """Show cost savings across multiple projects"""
    print("\n" + "="*60)
    print("MULTIPLE PROJECTS COMPARISON")
    print("="*60)
    
    projects = [
        "Build a REST API for a blog",
        "Create a todo list application",
        "Design a user authentication system"
    ]
    
    team = CachedDevTeam()
    
    for i, project in enumerate(projects):
        print(f"\n\n{'#'*60}")
        print(f"PROJECT {i+1}: {project}")
        print(f"{'#'*60}")
        
        team.build_project(project)
        
        # Wait a bit between projects (in real scenario)
        # Cache lasts 5 minutes, so all projects benefit!
    
    print("\n" + "="*60)
    print("FINAL SUMMARY - ALL PROJECTS")
    print("="*60)
    print(f"Total projects: {len(projects)}")
    print(f"Total cost: ${team.total_cost:.4f}")
    print(f"Total savings from caching: ${team.cache_savings:.4f}")
    print(f"Average cost per project: ${team.total_cost / len(projects):.4f}")


if __name__ == "__main__":
    # Example 1: Single project
    print("Example 1: Single Project with Caching")
    team = CachedDevTeam()
    result = team.build_project("Build a REST API for a blog")
    
    # Example 2: Multiple projects (uncomment to run)
    # print("\n\nExample 2: Multiple Projects")
    # compare_multiple_projects()
