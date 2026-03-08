# 🤖 AI Software Development Team

An automated software development team powered by AI agents that can generate complete projects from requirements.

## Features

- **Product Manager** - Analyzes requirements and creates PRD
- **Software Architect** - Designs system architecture
- **Senior Developer** - Writes implementation code
- **QA Tester** - Creates tests and validates quality
- **DevOps Engineer** - Sets up deployment configuration

## Real-time Progress Tracking

Watch each AI agent work in real-time with:
- Live status updates
- Progress bar showing completion
- Phase-by-phase tracking (1/5, 2/5, etc.)
- File save notifications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jyotigahan/SoftwareDEVAgenticAI.git
cd SoftwareDEVAgenticAI
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-openai-api-key-here
```

## Getting OpenAI API Key

1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API keys: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key and add it to your `.env` file

**Note**: You need to add credits to your OpenAI account for the API to work.

## Usage

### Run the Web UI

```bash
python app.py
```

Then open your browser to: http://127.0.0.1:7860

### Fill in the Form

1. **Programming Language/Framework** - Select your preferred tech stack
2. **Project Name** - Name for your project folder
3. **Requirement** - Describe what you want to build

### Click Generate

Watch the real-time progress as each agent works on your project!

## Output

The system generates:
- `01_requirements.md` - Product Requirements Document
- `02_architecture.md` - System Architecture Design
- `03_implementation.md` - Implementation Code
- `04_qa_tests.md` - QA Tests & Validation
- `05_deployment.md` - Deployment Guide
- `project_summary.json` - Project Summary
- `.zip` file - Complete project package

## Project Structure

```
SoftwareDEVAgenticAI/
├── agents/              # AI agent definitions
│   ├── product_manager.py
│   ├── architect.py
│   ├── developer.py
│   ├── qa_tester.py
│   └── devops.py
├── app.py              # Gradio web interface
├── orchestrator.py     # Workflow orchestration
├── crew_agents.py      # CrewAI agent setup
├── crew_tasks.py       # Task definitions
├── state.py            # State management
├── logger.py           # Logging system
└── requirements.txt    # Dependencies
```

## Technology Stack

- **CrewAI** - Multi-agent orchestration
- **OpenAI GPT-4o-mini** - AI model
- **Gradio** - Web interface
- **Python 3.8+** - Programming language

## Cost Estimation

Using GPT-4o-mini:
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Average project generation: $0.10 - $0.50

## Deployment

### Option 1: Hugging Face Spaces (Recommended)

1. Create account at https://huggingface.co
2. Create new Space with Gradio SDK
3. Upload your files
4. Add `OPENAI_API_KEY` in Space secrets
5. Deploy!

### Option 2: Railway.app

1. Create account at https://railway.app
2. Create new project from GitHub repo
3. Add `OPENAI_API_KEY` environment variable
4. Deploy!

### Option 3: Render.com

1. Create account at https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Add `OPENAI_API_KEY` environment variable
5. Deploy!

## Examples

### Example 1: REST API
```
Requirement: Create a REST API for a blog with user authentication, 
posts, comments, and likes. Include JWT authentication and PostgreSQL database.

Language: Python / FastAPI
```

### Example 2: Web App
```
Requirement: Build a todo list application with user accounts, 
task categories, due dates, and priority levels.

Language: React / Next.js
```

## Troubleshooting

### "Insufficient Quota" Error
- Add credits to your OpenAI account at https://platform.openai.com/account/billing

### Import Errors
- Make sure you're in the virtual environment
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Change the port in `app.py`: `demo.launch(server_port=7861)`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Author

Created by Jyoti Gahan

## Acknowledgments

- Built with [CrewAI](https://www.crewai.com/)
- Powered by [OpenAI](https://openai.com/)
- UI with [Gradio](https://gradio.app/)
