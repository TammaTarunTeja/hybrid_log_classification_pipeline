import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
groq_api_key = os.getenv("LLM_KEY") # Ensure this matches your .env key

def llm_classifier(log_message: str, is_legacy: bool) -> str:
    client = Groq(api_key=groq_api_key)
    
    regex_labels = [
        "HTTP Status", "Security Alert", "System Notification", 
        "Error", "Resource Usage", "Critical Error", 
        "User Action"
    ]
    legacy_labels = [
        "Workflow Error"
        "Deprecation Warning"
    ]
    if is_legacy:
        labels = legacy_labels
    else:
        labels = regex_labels
    # System prompt strictly defines the output format
    system_prompt = "You are a log classifier. Your output MUST be exactly one label from the provided list. Do not include explanations or conversational text.if the log message does not match any label, respond with 'Unknown'."
    
    user_prompt = f"""Classify this log message.
Available labels: {', '.join(labels)}

Log message: {log_message}

Target Label:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,   
        max_tokens=20       
    )
    
    return response.choices[0].message.content.strip()

# Sample log messages for testing
if __name__ == "__main__":
    test_logs = [
        "nova.osapi_compute.wsgi.server started successfully.",
        "nova.compute.claims resource allocation failed.",
        "User User123 logged in.",
        "Backup started for server instance 456.",
        "Multiple bad login attempts detected from IP 192.168.1.100."   ]  
    for log in test_logs:
        label = llm_classifier(log, is_regex= True)
        print(f"Log: '{log}' => Classified as: {label}")