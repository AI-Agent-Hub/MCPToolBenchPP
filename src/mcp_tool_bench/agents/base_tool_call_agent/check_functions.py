import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, '../')))
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_DIR, './')))

from src.mcp_tool_bench.agents.base_tool_call_agent.prompt import *

import html
import re
from bs4 import BeautifulSoup
from src.mcp_tool_bench.global_variables import *
from src.mcp_tool_bench.model_utils.model_provider import _global_model_provider
from src.mcp_tool_bench.model_utils.base_api import *
import json
import logging
from typing import List, Dict, Tuple
from tqdm import tqdm

def decode_html_entities(s):
    """Decode HTML entities"""
    # Try using html.unescape
    first_decode = html.unescape(s)
    # Check if still contains undecoded entities
    if "&" in first_decode and ";" in first_decode:
        # Use BeautifulSoup for further decoding
        soup = BeautifulSoup(first_decode, "html.parser")
        second_decode = soup.get_text()
        return second_decode
    return first_decode

def auto_fix_unclosed_quotes(data):
    """
    Automatically detect and fix unclosed quotes in strings.
    """
    if isinstance(data, list):
        return data

    """
    Automatically add space after colon in key-value pairs, e.g., convert 'key:value' to 'key: value'
    """
    # Use regex to match cases where colon is not followed by space, and add space
    data = re.sub(r'(?m)^(\s*[^#\s][^:]*):([^\s])', r'\1: \2', data)
    
    lines = data.split("\n")
    fixed_lines = []
    for line in lines:
        # Detect and fix unclosed quotes
        if line.count('"') % 2 != 0:
            line = line + '"'  # Append a quote to close
        fixed_lines.append(line)
    return "\n".join(fixed_lines)

def process_response(response_text):
    """Process GPT response text"""
    if not response_text:
        return ""
    
    raw_val = decode_html_entities(response_text)
    raw_val = auto_fix_unclosed_quotes(raw_val)
    decoded_json_str = html.unescape(raw_val)
    decoded_json_str = decoded_json_str.replace("```json\n", "").replace("```", "").replace("\n", "")
    return decoded_json_str

def check_ast(pred_tool_result_list: List[Dict], label_result_list: List[Dict]) -> Tuple[bool, bool]:
    """
    Check the AST of tool calls
    """
    label_step = len(label_result_list) if label_result_list is not None else 0
    predict_step = len(pred_tool_result_list) if pred_tool_result_list is not None else 0
    if (label_step == 1 and predict_step == 1):
        user_prompt = user_prompt_template_ast.format(pred_tool_result_list=pred_tool_result_list, label_result_list=label_result_list)
        system_prompt = system_prompt_template_ast.format()
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        # print("messages: ", messages)
        model_provider = _global_model_provider[MODEL_SELECTION_GPT4O_ANT] if MODEL_SELECTION_GPT4O_ANT in _global_model_provider else None
        output = model_provider.api_chat(messages, wait_time=5) if model_provider is not None else {}
        raw_response = output[KEY_COMPLETION] if KEY_COMPLETION in output else ""
        # Normal chat: process string
        if isinstance(raw_response, str):
            result =  process_response(raw_response)
        try:
            result = json.loads(result)
        except Exception as e:
            logging.error(f" Failed to parse json {e}")
            return False, False
        
        tool_correctness = result["tool_correctness"] if "tool_correctness" in result else 0
        parameter_correctness = result["parameter_correctness"] if "parameter_correctness" in result else 0
        
    elif (label_step == 1 and predict_step > 1):
        return False, False
    elif (label_step > 1 and predict_step == 1):
        return False, False
    else:
        ## multiple
        return False, False
    return tool_correctness, parameter_correctness

if __name__ == "__main__":
    # Read the input JSON file
    input_file_path = "logs/browser/browser_0711_single_500_20250713_080044.json"
    output_file_path = "logs/browser/browser_0711_single_500_20250713_080044_ast.json"
    # input_file_path = "logs/browser/test_log.json"
    # output_file_path = "logs/browser/test_log_ast.json"
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Calculate total number of function calls to process
        total_function_calls = 0
        for run_detail in data.get("run_details", []):
            for trial in run_detail.get("trials", []):
                total_function_calls += len(trial.get("function_call_result", []))
        
        print(f"Total function calls to process: {total_function_calls}")
        
        # Process each run_detail with progress bar
        processed_calls = 0
        for run_detail in tqdm(data.get("run_details", []), desc="Processing run_details"):
            function_call_label = run_detail.get("function_call_label", [])
            
            # Process each trial
            for trial in run_detail.get("trials", []):
                function_call_results = trial.get("function_call_result", [])
                
                # Call check_ast with function_call_label and function_call_result
                tool_correctness, parameter_correctness = check_ast(
                    function_call_results, 
                    function_call_label
                )
                
                # Add the new fields to function_call_result
                trial["tool_correctness"] = True if tool_correctness == 1 else False
                trial["parameter_correctness"] = True if parameter_correctness == 1 else False
                
                processed_calls += 1
        
        # Write the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Processing completed. Output written to {output_file_path}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file_path} not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
    except Exception as e:
        print(f"Error: {e}")
