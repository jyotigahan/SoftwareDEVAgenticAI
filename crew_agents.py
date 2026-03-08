"""CrewAI agent definitions for the software development team."""

from crewai import Agent
from logger import AgentLogger

logger = AgentLogger()


def create_product_manager() -> Agent:
    """Create Product Manager agent using CrewAI."""
    logger.info("🔧 Creating Product Manager agent...")
    
    return Agent(
        role='Product Manager',
        goal='Analyze user requirements and create comprehensive product specifications',
        backstory="""You are an experienced Product Manager with 10+ years in software development.
        You excel at understanding user needs, defining clear requirements, and creating detailed 
        product requirement documents (PRD). You think about user stories, acceptance criteria, 
        and success metrics. You ensure all stakeholders understand what needs to be built.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_architect() -> Agent:
    """Create Architect agent using CrewAI."""
    logger.info("🔧 Creating Architect agent...")
    
    return Agent(
        role='Software Architect',
        goal='Design robust, scalable system architecture based on requirements',
        backstory="""You are a Senior Software Architect with expertise in system design, 
        microservices, databases, and cloud architecture. You make informed decisions about 
        technology stack, design patterns, data models, and API structures. You consider 
        scalability, security, maintainability, and performance in all your designs.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_developer() -> Agent:
    """Create Developer agent using CrewAI."""
    logger.info("🔧 Creating Developer agent...")
    
    return Agent(
        role='Senior Software Developer',
        goal='Write clean, efficient, and well-documented production-ready code',
        backstory="""You are a Senior Software Developer with expertise in multiple programming 
        languages and frameworks. You write clean, maintainable code following best practices 
        and design patterns. You include proper error handling, input validation, and comprehensive 
        documentation. Your code is production-ready and follows industry standards.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_qa_tester() -> Agent:
    """Create QA Tester agent using CrewAI."""
    logger.info("🔧 Creating QA Tester agent...")
    
    return Agent(
        role='QA Engineer',
        goal='Ensure code quality through comprehensive testing and validation',
        backstory="""You are a Senior QA Engineer with expertise in test automation, quality 
        assurance, and software testing methodologies. You create thorough test cases, write 
        automated tests, identify edge cases and potential bugs. You validate that all acceptance 
        criteria are met and the implementation matches requirements.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_devops() -> Agent:
    """Create DevOps agent using CrewAI."""
    logger.info("🔧 Creating DevOps agent...")
    
    return Agent(
        role='DevOps Engineer',
        goal='Create deployment configurations and infrastructure setup',
        backstory="""You are a Senior DevOps Engineer with expertise in containerization, 
        CI/CD pipelines, cloud infrastructure, and deployment automation. You create Docker 
        configurations, CI/CD pipelines, infrastructure as code, and deployment scripts. 
        You ensure applications are secure, scalable, and easy to deploy.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
