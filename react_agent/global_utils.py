from datetime import datetime
import os
import platform

from react_agent.core.llm_config import LLMSettings, get_llm_settings


def get_operating_system_name() -> str:
    os_map = {
        "Darwin": "macOS",
        "Windows": "Windows",
        "Linux": "Linux",
    }
    return os_map.get(platform.system(), "Unknown")


def get_api_key() -> str:
    return get_llm_settings().api_key


def get_llm_model_name() -> str:
    return get_llm_settings().model


def get_llm_config() -> LLMSettings:
    return get_llm_settings()

def write_log(message: str, log_dir="log"):
    os.makedirs(log_dir, exist_ok=True)
    
    filename = datetime.now().strftime("%Y-%m-%d") + ".txt"
    log_path = os.path.join(log_dir, filename)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return log_path
        