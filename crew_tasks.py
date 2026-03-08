"""CrewAI task definitions for the software development workflow."""

from crewai import Task
from logger import AgentLogger

logger = AgentLogger()


def create_pm_task(agent, requirement: str, language: str) -> Task:
    """Create Product Manager task."""
    logger.agent_start("Product Manager", f"Requirement: {requirement} | Language: {language}")
    
    return Task(
        description=f"""Analyze the following requirement and create a comprehensive Product Requirements Document (PRD):

Requirement: {requirement}
Target Programming Language/Framework: {language}

Your PRD must include:
1. Project Overview - Brief description of what we're building
2. Target Technology - State the requested language/framework and ensure the requirements align with it
3. User Stories - At least 3-5 user stories with acceptance criteria
4. Core Features - List of main features with descriptions
5. Functional Requirements - Specific functional requirements
6. Non-Functional Requirements - Performance, security, scalability needs
7. Success Metrics - How we'll measure success
8. API Endpoints - List of required API endpoints (if applicable)

Be specific, clear, and comprehensive. Focus on WHAT needs to be built, and keep the requested language in mind.""",
        agent=agent,
        expected_output="""A detailed Product Requirements Document in markdown format with all sections:
- Project Overview
- Target Technology
- User Stories with acceptance criteria
- Core Features list
- Functional Requirements
- Non-Functional Requirements
- Success Metrics
- API Endpoints (if applicable)"""
    )


def create_architect_task(agent, prd_content: str) -> Task:
    """Create Architect task."""
    logger.agent_start("Architect", "Design system architecture")
    
    return Task(
        description=f"""Based on the following Product Requirements Document, design a comprehensive system architecture.

PRD Context:
{prd_content}

Your architecture document must include:
1. Technology Stack - Specific languages, frameworks, databases, tools
2. System Architecture - High-level architecture description
3. Data Models - Database schema with fields and types
4. API Design - Detailed API endpoints with methods, paths, request/response formats
5. Component Structure - Project folder structure and file organization
6. Security Considerations - Authentication, authorization, data protection
7. Scalability & Performance - How the system will scale

Provide specific technical decisions with rationale. Be detailed and practical.""",
        agent=agent,
        expected_output="""A comprehensive Architecture Design Document in markdown format including:
- Technology Stack with specific versions
- System Architecture diagram/description
- Complete Data Models with all fields
- Detailed API Design with all endpoints
- Component/Folder Structure
- Security implementation plan
- Scalability considerations"""
    )


def create_developer_task(agent, prd_content: str, architecture_content: str) -> Task:
    """Create Developer task."""
    logger.agent_start("Developer", "Implement the system")
    
    return Task(
        description=f"""Based on the Architecture Design, implement the complete system.

PRD Context:
{prd_content}

Architecture Context:
{architecture_content}

Your implementation must include:
1. All source code files with complete, working code
2. Proper project structure as defined in architecture
3. Error handling and input validation
4. Inline comments for complex logic
5. Configuration files (package.json, requirements.txt, etc.)
6. README with setup instructions
7. Example usage code

Provide COMPLETE, production-ready code that can be run immediately.
Include all necessary imports, dependencies, and configurations.
Write clean, maintainable code following best practices.""",
        agent=agent,
        expected_output="""Complete implementation with:
- All source code files (models, routes, controllers, services)
- Configuration files
- Dependencies file
- Setup instructions
- Usage examples
All code must be complete, working, and production-ready."""
    )


def create_qa_task(agent, prd_content: str, architecture_content: str, implementation_content: str) -> Task:
    """Create QA Tester task."""
    logger.agent_start("QA Tester", "Create tests and validate quality")
    
    return Task(
        description=f"""Review the requirements and implementation, then create comprehensive tests.

PRD Context:
{prd_content}

Architecture Context:
{architecture_content}

Implementation Context:
{implementation_content}

Your test report must include:
1. Test Strategy - Overview of testing approach
2. Test Cases - Detailed test cases with steps and expected results
3. Unit Tests - Complete unit test code for all components
4. Integration Tests - API/integration test code
5. Edge Cases - Identified edge cases and potential issues
6. Test Coverage Analysis - Coverage assessment for each component
7. Acceptance Criteria Validation - Check each criteria from PRD

Provide executable test code and thorough quality analysis.
Identify any bugs, issues, or improvements needed.""",
        agent=agent,
        expected_output="""Comprehensive QA Test Report including:
- Test Strategy
- Detailed Test Cases
- Complete Unit Test code
- Integration Test code
- Edge Cases identified
- Test Coverage Analysis
- Acceptance Criteria validation results"""
    )


def create_devops_task(agent, architecture_content: str, implementation_content: str) -> Task:
    """Create DevOps task."""
    logger.agent_start("DevOps", "Create deployment configurations")
    
    return Task(
        description=f"""Based on the architecture and implementation, create complete deployment setup.

Architecture Context:
{architecture_content}

Implementation Context:
{implementation_content}

Your deployment guide must include:
1. Dockerfile - Complete, working Dockerfile
2. docker-compose.yml - Complete docker-compose configuration
3. CI/CD Pipeline - GitHub Actions or similar CI/CD config
4. Environment Configuration - .env.example with all variables
5. Deployment Instructions - Step-by-step for local and production
6. Infrastructure Requirements - Server specs, services needed
7. Monitoring & Logging - Setup for monitoring and logs
8. Security Checklist - Security measures to implement

Provide complete, production-ready deployment configurations.
All files should be ready to use without modifications.""",
        agent=agent,
        expected_output="""Complete DevOps Deployment Guide including:
- Working Dockerfile
- docker-compose.yml
- CI/CD pipeline configuration
- Environment configuration template
- Detailed deployment instructions
- Infrastructure requirements
- Monitoring/logging setup
- Security checklist"""
    )
