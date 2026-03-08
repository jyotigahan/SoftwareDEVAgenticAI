"""Email notification system for stage completion."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class EmailNotifier:
    """Handles email notifications for stage completions."""
    
    def __init__(self, recipient_email: str):
        self.recipient_email = recipient_email
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_email = os.getenv("SMTP_EMAIL")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        # Check if email is configured
        self.enabled = bool(self.smtp_email and self.smtp_password)
        
        if not self.enabled:
            print("⚠️  Email notifications disabled (SMTP credentials not configured)")
    
    def send_stage_completion(self, stage: str, agent: str, summary: str, output_file: str = None):
        """Send email notification when a stage completes."""
        if not self.enabled:
            print(f"📧 [MOCK] Would send email: {stage} completed by {agent}")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"✅ {stage} Completed - AI Development Team"
            msg['From'] = self.smtp_email
            msg['To'] = self.recipient_email
            
            # Email body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            text_body = f"""
AI Development Team - Stage Completion Notification

Stage: {stage}
Agent: {agent}
Completed: {timestamp}

Summary:
{summary}

{'Output saved to: ' + output_file if output_file else ''}

---
This is an automated notification from your AI Development Team.
"""
            
            html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
        .stage {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .agent {{ color: #667eea; font-weight: bold; }}
        .summary {{ background: white; padding: 15px; border-left: 4px solid #667eea; 
                    margin: 15px 0; white-space: pre-wrap; }}
        .footer {{ background: #333; color: white; padding: 10px; text-align: center; 
                   border-radius: 0 0 8px 8px; font-size: 12px; }}
        .timestamp {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="stage">✅ {stage} Completed</div>
            <div class="timestamp">🕐 {timestamp}</div>
        </div>
        <div class="content">
            <p><strong>Agent:</strong> <span class="agent">{agent}</span></p>
            
            <div class="summary">
                <strong>Summary:</strong><br>
                {summary}
            </div>
            
            {f'<p><strong>📁 Output:</strong> {output_file}</p>' if output_file else ''}
        </div>
        <div class="footer">
            This is an automated notification from your AI Development Team
        </div>
    </div>
</body>
</html>
"""
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
            
            print(f"📧 Email sent to {self.recipient_email}: {stage} completed")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to send email: {str(e)}")
            return False
    
    def send_project_complete(self, project_name: str, output_dir: str, files: list):
        """Send final email when entire project is complete."""
        if not self.enabled:
            print(f"📧 [MOCK] Would send project completion email")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎉 Project Complete: {project_name}"
            msg['From'] = self.smtp_email
            msg['To'] = self.recipient_email
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            files_list = "\n".join([f"  • {f}" for f in files])
            
            text_body = f"""
🎉 PROJECT COMPLETE!

Project: {project_name}
Completed: {timestamp}

All stages have been completed successfully by your AI Development Team.

Generated Files:
{files_list}

Output Directory: {output_dir}

Your project is ready for review!

---
AI Development Team
"""
            
            html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                   color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
        .title {{ font-size: 32px; font-weight: bold; margin-bottom: 10px; }}
        .files {{ background: white; padding: 15px; border-left: 4px solid #11998e; margin: 15px 0; }}
        .files ul {{ list-style: none; padding: 0; }}
        .files li {{ padding: 5px 0; }}
        .footer {{ background: #333; color: white; padding: 10px; text-align: center; 
                   border-radius: 0 0 8px 8px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🎉 PROJECT COMPLETE!</div>
            <div>{timestamp}</div>
        </div>
        <div class="content">
            <p><strong>Project:</strong> {project_name}</p>
            <p>All stages have been completed successfully by your AI Development Team.</p>
            
            <div class="files">
                <strong>📁 Generated Files:</strong>
                <ul>
                    {''.join([f'<li>✓ {f}</li>' for f in files])}
                </ul>
            </div>
            
            <p><strong>Output Directory:</strong> <code>{output_dir}</code></p>
            <p style="color: #11998e; font-weight: bold;">Your project is ready for review! 🚀</p>
        </div>
        <div class="footer">
            AI Development Team - Powered by CrewAI
        </div>
    </div>
</body>
</html>
"""
            
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
            
            print(f"📧 Project completion email sent to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to send email: {str(e)}")
            return False
