"""Orchestrator that coordinates the agent workflow using CrewAI."""

import os
from crewai import Crew, Process
from crew_agents import (
    create_product_manager,
    create_architect,
    create_developer,
    create_qa_tester,
    create_devops
)
from crew_tasks import (
    create_pm_task,
    create_architect_task,
    create_developer_task,
    create_qa_task,
    create_devops_task
)
from state import ProjectState
from email_notifier import EmailNotifier
from logger import AgentLogger


class TeamOrchestrator:
    """Orchestrates the software development team workflow using CrewAI."""
    
    def __init__(self, recipient_email: str = None, project_name: str = "my_project"):
        self.logger = AgentLogger()
        self.project_name = project_name
        self.zip_path = None
        
        # Save output inside a folder named after the project
        output_dir = os.path.join(os.getcwd(), project_name)
        self.state = ProjectState(output_dir=output_dir)
        
        self.email_notifier = EmailNotifier(recipient_email) if recipient_email else None
        
        self.logger.info("🚀 Initializing AI Development Team with CrewAI...")
        
        # Create agents
        self.pm_agent = create_product_manager()
        self.architect_agent = create_architect()
        self.developer_agent = create_developer()
        self.qa_agent = create_qa_tester()
        self.devops_agent = create_devops()
        
        self.logger.info("✅ All agents created successfully\n")
    
    def get_zip_path(self):
        """Return the path to the generated zip file."""
        return self.zip_path
    
    def run_with_progress(self, user_requirement: str, language: str = "Any"):
        """Execute the complete development workflow with progress updates."""
        self.logger.info("="*60)
        self.logger.info("🚀 AUTOMATED SOFTWARE DEVELOPMENT TEAM (CrewAI)")
        self.logger.info("="*60)
        self.logger.info(f"📁 Project Name: {self.project_name}")
        self.logger.info(f"📋 Requirement: {user_requirement}")
        self.logger.info(f"💻 Language: {language}\n")
        
        try:
            # Phase 1: Product Management
            yield "📋 Phase 1/5: Product Manager analyzing requirements..."
            for update in self._run_phase_with_progress(
                phase_name="Product Management",
                agent=self.pm_agent,
                task_creator=lambda: create_pm_task(self.pm_agent, user_requirement, language),
                output_file="01_requirements.md",
                artifact_type="PRD"
            ):
                yield update
            yield "✅ Product Manager completed - Requirements documented"
            prd_content = self.state.get_artifact("Product Manager", "PRD")
            
            # Phase 2: Architecture Design
            yield "\n🏗️ Phase 2/5: Software Architect designing system..."
            for update in self._run_phase_with_progress(
                phase_name="Architecture Design",
                agent=self.architect_agent,
                task_creator=lambda: create_architect_task(self.architect_agent, prd_content),
                output_file="02_architecture.md",
                artifact_type="Architecture"
            ):
                yield update
            yield "✅ Architect completed - System architecture designed"
            architecture_content = self.state.get_artifact("Software Architect", "Architecture")
            
            # Phase 3: Development
            yield "\n💻 Phase 3/5: Senior Developer writing implementation code..."
            for update in self._run_phase_with_progress(
                phase_name="Development",
                agent=self.developer_agent,
                task_creator=lambda: create_developer_task(self.developer_agent, prd_content, architecture_content),
                output_file="03_implementation.md",
                artifact_type="Code"
            ):
                yield update
            yield "✅ Developer completed - Code implementation ready"
            implementation_content = self.state.get_artifact("Senior Software Developer", "Code")
            
            # Phase 4: QA Testing
            yield "\n🧪 Phase 4/5: QA Tester validating and creating tests..."
            for update in self._run_phase_with_progress(
                phase_name="QA Testing",
                agent=self.qa_agent,
                task_creator=lambda: create_qa_task(self.qa_agent, prd_content, architecture_content, implementation_content),
                output_file="04_qa_tests.md",
                artifact_type="Tests"
            ):
                yield update
            yield "✅ QA completed - Tests created and validated"
            
            # Phase 5: DevOps
            yield "\n🚀 Phase 5/5: DevOps Engineer setting up deployment..."
            for update in self._run_phase_with_progress(
                phase_name="DevOps & Deployment",
                agent=self.devops_agent,
                task_creator=lambda: create_devops_task(self.devops_agent, architecture_content, implementation_content),
                output_file="05_deployment.md",
                artifact_type="Deployment"
            ):
                yield update
            yield "✅ DevOps completed - Deployment configuration ready"
            
            # Complete
            yield "\n📦 Finalizing project..."
            self.state.set_phase("Complete")
            self.state.save_summary()
            
            # Send final email
            if self.email_notifier:
                files = [
                    "01_requirements.md",
                    "02_architecture.md",
                    "03_implementation.md",
                    "04_qa_tests.md",
                    "05_deployment.md",
                    "project_summary.json"
                ]
                self.email_notifier.send_project_complete(
                    self.project_name,
                    self.state.output_dir,
                    files
                )
            
            # Create a zip archive of the output directory
            import shutil
            self.zip_path = shutil.make_archive(
                base_name=self.state.output_dir,
                format='zip',
                root_dir=self.state.output_dir
            )
            
            yield f"📦 Project packaged: {self.zip_path}"
            
            self.logger.info("\n" + "="*60)
            self.logger.info("✅ PROJECT COMPLETE!")
            self.logger.info("="*60)
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            raise
    
    def _run_phase_with_progress(self, phase_name: str, agent, task_creator, output_file: str, 
                                  artifact_type: str):
        """Run a single phase of the workflow with progress updates."""
        self.state.set_phase(phase_name)
        self.logger.phase_start(phase_name)
        
        # Create task
        task = task_creator()
        
        # Create crew for this phase
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute
        yield f"  🔄 {agent.role} is working..."
        result = crew.kickoff()
        
        # Extract result
        output = str(result)
        self.logger.agent_complete(agent.role, len(output))
        
        # Save artifact
        self.state.add_artifact(agent.role, artifact_type, output, output_file)
        yield f"  💾 Saved: {output_file}"
        
        # Send email notification
        if self.email_notifier:
            summary = output[:500] + "..." if len(output) > 500 else output
            self.email_notifier.send_stage_completion(
                phase_name,
                agent.role,
                summary,
                output_file
            )
            self.logger.email_sent(self.email_notifier.recipient_email, f"{phase_name} completed")
        
        self.logger.info(f"✅ {phase_name} completed\n")
    
    def run(self, user_requirement: str, language: str = "Any"):
        """Execute the complete development workflow."""
        self.logger.info("="*60)
        self.logger.info("🚀 AUTOMATED SOFTWARE DEVELOPMENT TEAM (CrewAI)")
        self.logger.info("="*60)
        self.logger.info(f"📁 Project Name: {self.project_name}")
        self.logger.info(f"📋 Requirement: {user_requirement}")
        self.logger.info(f"💻 Language: {language}\n")
        
        try:
            # Phase 1: Product Management
            self._run_phase(
                phase_name="Product Management",
                agent=self.pm_agent,
                task_creator=lambda: create_pm_task(self.pm_agent, user_requirement, language),
                output_file="01_requirements.md",
                artifact_type="PRD"
            )
            prd_content = self.state.get_artifact("Product Manager", "PRD")
            
            # Phase 2: Architecture Design
            self._run_phase(
                phase_name="Architecture Design",
                agent=self.architect_agent,
                task_creator=lambda: create_architect_task(self.architect_agent, prd_content),
                output_file="02_architecture.md",
                artifact_type="Architecture"
            )
            architecture_content = self.state.get_artifact("Software Architect", "Architecture")
            
            # Phase 3: Development
            self._run_phase(
                phase_name="Development",
                agent=self.developer_agent,
                task_creator=lambda: create_developer_task(self.developer_agent, prd_content, architecture_content),
                output_file="03_implementation.md",
                artifact_type="Code"
            )
            implementation_content = self.state.get_artifact("Senior Software Developer", "Code")
            
            # Phase 4: QA Testing
            self._run_phase(
                phase_name="QA Testing",
                agent=self.qa_agent,
                task_creator=lambda: create_qa_task(self.qa_agent, prd_content, architecture_content, implementation_content),
                output_file="04_qa_tests.md",
                artifact_type="Tests"
            )
            
            # Phase 5: DevOps
            self._run_phase(
                phase_name="DevOps & Deployment",
                agent=self.devops_agent,
                task_creator=lambda: create_devops_task(self.devops_agent, architecture_content, implementation_content),
                output_file="05_deployment.md",
                artifact_type="Deployment"
            )
            
            # Complete
            self.state.set_phase("Complete")
            self.state.save_summary()
            
            # Send final email
            if self.email_notifier:
                files = [
                    "01_requirements.md",
                    "02_architecture.md",
                    "03_implementation.md",
                    "04_qa_tests.md",
                    "05_deployment.md",
                    "project_summary.json"
                ]
                self.email_notifier.send_project_complete(
                    self.project_name,
                    self.state.output_dir,
                    files
                )
            
            # Create a zip archive of the output directory
            import shutil
            self.zip_path = shutil.make_archive(
                base_name=self.state.output_dir,
                format='zip',
                root_dir=self.state.output_dir
            )
            
            self.logger.info("\n" + "="*60)
            self.logger.info("✅ PROJECT COMPLETE!")
            self.logger.info("="*60)
            self.logger.info(f"\n📁 All artifacts saved in: {self.state.output_dir}/")
            self.logger.info(f"📦 Zipped artifacts saved in: {self.zip_path}")
            self.logger.info(f"📋 Activity log saved in: {self.logger.get_log_file()}")
            self.logger.info("\nGenerated files:")
            self.logger.info("  1. 01_requirements.md - Product Requirements")
            self.logger.info("  2. 02_architecture.md - System Architecture")
            self.logger.info("  3. 03_implementation.md - Implementation Code")
            self.logger.info("  4. 04_qa_tests.md - QA Tests & Validation")
            self.logger.info("  5. 05_deployment.md - Deployment Guide")
            self.logger.info("  6. project_summary.json - Project Summary\n")
            
            return self.zip_path
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            raise
    
    def _run_phase(self, phase_name: str, agent, task_creator, output_file: str, 
                   artifact_type: str):
        """Run a single phase of the workflow."""
        self.state.set_phase(phase_name)
        self.logger.phase_start(phase_name)
        
        # Create task
        task = task_creator()
        
        # Create crew for this phase
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute
        self.logger.info(f"🔄 Executing {phase_name}...")
        result = crew.kickoff()
        
        # Extract result
        output = str(result)
        self.logger.agent_complete(agent.role, len(output))
        
        # Save artifact
        self.state.add_artifact(agent.role, artifact_type, output, output_file)
        
        # Send email notification
        if self.email_notifier:
            summary = output[:500] + "..." if len(output) > 500 else output
            self.email_notifier.send_stage_completion(
                phase_name,
                agent.role,
                summary,
                output_file
            )
            self.logger.email_sent(self.email_notifier.recipient_email, f"{phase_name} completed")
        
        self.logger.info(f"✅ {phase_name} completed\n")
