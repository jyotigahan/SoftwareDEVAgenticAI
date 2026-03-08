"""Project state management for tracking artifacts and progress."""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


class ProjectState:
    """Manages the state of the software development project."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.artifacts: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
        self.current_phase = "initialization"
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def add_artifact(self, agent: str, artifact_type: str, content: str, filename: str = None):
        """Store an artifact produced by an agent."""
        timestamp = datetime.now().isoformat()
        
        artifact = {
            "agent": agent,
            "type": artifact_type,
            "content": content,
            "timestamp": timestamp,
            "filename": filename
        }
        
        key = f"{agent}_{artifact_type}"
        self.artifacts[key] = artifact
        self.history.append(artifact)
        
        # Save to file if filename provided
        if filename:
            filepath = os.path.join(self.output_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  💾 Saved: {filepath}")
    
    def get_artifact(self, agent: str, artifact_type: str) -> str:
        """Retrieve an artifact by agent and type."""
        key = f"{agent}_{artifact_type}"
        artifact = self.artifacts.get(key)
        return artifact["content"] if artifact else None
    
    def set_phase(self, phase: str):
        """Update the current project phase."""
        self.current_phase = phase
        print(f"\n{'='*60}")
        print(f"📍 Phase: {phase.upper()}")
        print(f"{'='*60}\n")
    
    def save_summary(self):
        """Save a summary of all artifacts."""
        summary = {
            "project_phase": self.current_phase,
            "artifacts": list(self.artifacts.keys()),
            "history": self.history
        }
        
        filepath = os.path.join(self.output_dir, "project_summary.json")
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Project summary saved: {filepath}")
