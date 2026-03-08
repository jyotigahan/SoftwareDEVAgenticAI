"""Main entry point for the Automated Software Development Team."""

import os
from dotenv import load_dotenv
from orchestrator import TeamOrchestrator


def main():
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found!")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("\nOr create a .env file with:")
        print("  OPENAI_API_KEY=your-key-here")
        return
    
    print("\n" + "="*60)
    print("  AUTOMATED SOFTWARE DEVELOPMENT TEAM (CrewAI)")
    print("="*60)
    print("\nThis AI team will:")
    print("  1. 📋 Product Manager - Analyze requirements")
    print("  2. 🏗️  Architect - Design system")
    print("  3. 💻 Developer - Write code")
    print("  4. 🧪 QA Tester - Create tests")
    print("  5. 🚀 DevOps - Setup deployment")
    print("\n  📧 Email notifications at each stage")
    print("  📋 Detailed activity logging")
    print()
    
    # Get email for notifications
    print("Enter your email for stage completion notifications:")
    print("(Press Enter to skip email notifications)")
    email = input("Email: ").strip()
    
    if email and '@' not in email:
        print("⚠️  Invalid email format. Continuing without email notifications.")
        email = None
    
    if email:
        print(f"✅ Email notifications will be sent to: {email}")
        smtp_configured = os.getenv("SMTP_EMAIL") and os.getenv("SMTP_PASSWORD")
        if not smtp_configured:
            print("⚠️  SMTP credentials not configured in .env file")
            print("   Email notifications will be mocked (not actually sent)")
            print("   To enable real emails, add to .env:")
            print("     SMTP_EMAIL=your-email@gmail.com")
            print("     SMTP_PASSWORD=your-app-password")
    print()
    
    # Get user requirement
    print("What would you like to build?")
    print("Example: 'A REST API for a blog'")
    print()
    requirement = input("Your requirement: ").strip()
    
    if not requirement:
        print("❌ No requirement provided. Exiting.")
        return
        
    print("\nWhat programming language/framework would you prefer?")
    print("Example: 'Python/FastAPI', 'Node.js/Express', 'Go', or press Enter for 'Any'")
    language = input("Language preference: ").strip()
    if not language:
        language = "Any"
        
    print("\nWhat is the name of your project? (This will be the folder name)")
    print("Example: 'blog-api'")
    project_name = input("Project name: ").strip()
    if not project_name:
        project_name = "my_ai_project"
    
    # Clean up project name for folder use
    folder_name = "".join([c if c.isalnum() or c in ['-', '_'] else '_' for c in project_name])
    
    print("\n🚀 Starting development workflow...\n")
    
    # Run the team
    orchestrator = TeamOrchestrator(recipient_email=email, project_name=folder_name)
    
    try:
        zip_path = orchestrator.run(requirement, language)
        if zip_path:
            print("\n" + "="*60)
            print("🎁 YOUR PROJECT IS READY FOR DOWNLOAD!")
            print("="*60)
            print(f"To access your generated files, grab the zip folder here:")
            print(f"👉 {zip_path}")
            print("\nOr navigate to the extracted folder:")
            print(f"👉 {os.path.join(os.getcwd(), folder_name)}")
            print("="*60 + "\n")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user.")
        return
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("  - Your OpenAI API key is valid")
        print("  - You have internet connection")
        print("  - Check the logs/ directory for detailed error logs")
        return


if __name__ == "__main__":
    main()
