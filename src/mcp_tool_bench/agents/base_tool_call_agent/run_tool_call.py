import uuid
import json
import logging
import requests
import os
import datetime
from typing import List, Dict, Any, Tuple
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import requests

from src.mcp_tool_bench.global_variables import *
from src.mcp_tool_bench.model_utils.model_provider import _global_model_provider
from src.mcp_tool_bench.evaluation.evaluation_utils import _global_tool_result_check_func_provider, base_compare_result, estimate_pass_at_k
from src.mcp_tool_bench.common_utils import *
from src.mcp_tool_bench.model_utils.base_api import *
from src.mcp_tool_bench.agents.base_tool_call_agent.check_functions import check_ast

def rev_tool_servername_dict(mcp_server_tools):
    """
        Args:
            mcp_server_tools: 
            key: server_name, value, list of tool_name
        
        Return:
            Dict, key: tool_name, value: server_name
            if tool_name conflicts, add {server_name}_{tool_name} as tool_name
    """
    tool_to_servername_dict = {}
    for key, value in mcp_server_tools.items():
        for tool_name in value:
            if tool_name in tool_to_servername_dict:
                tool_to_servername_dict[key + "_" + tool_name] = key
            else:
                tool_to_servername_dict[tool_name] = key
    return tool_to_servername_dict

def agent_loop(query: str, tools: List[Dict], model: str, **kwargs) -> List[Dict]:
    """
    Agent loop for executing tool calls
    
    Args:
        query: User query
        tools: Available tools list
        model: Model name
        **kwargs: Other parameters
        
    Returns:
        List[Dict]: Tool Call Result Node, 
        function_call_result.append({
            "id": tool_id,
            "name": tool_name,
            "input": tool_arguments,
            "output": tool_result,
            "status_code": status_code
        })
    """

    tool_result_list = []
    
    mcp_tools_dict = kwargs[KEY_MCP_TOOLS_DICT] if KEY_MCP_TOOLS_DICT in kwargs else {}
    mcp_tools_dict = rev_tool_servername_dict(mcp_tools_dict)

    ## claude format to OpenAI format

    # print (f"tools type {type(tools)} and result {tools}")

    # toolname to servername dict
    iterations = 0
    max_iterations = 2

    call_messages = [
        {"role": "user", "content": query}
    ]
    # save the function call sequence result
    function_call_result = []
    loop_end = False
    while ((not loop_end) and iterations <= max_iterations):
        iterations += 1
        # print (f"Running Iterations {iterations}")

        # tools schema wrapper
        tools_mapped = tools_schema_wrapper(model, tools)
        # print (f"agent_loop tools type {type(tools)} and result {tools}")

        tool_call = call_llm_tools_function_call_wrapper(model, {"messages": call_messages, "tools": tools_mapped})
        print (f"Iteration {iterations} agent_loop tool_call result {tool_call}")

        if tool_call is None or len(tool_call) == 0:
            # no tools selected, end of function call
            logging.info(f"Iteration {iterations} No Tools Chosen by LLM tool_call tool_call {tool_call}")
            loop_end = True 

        else:
            # print (f"DEBUG: tool_call {tool_call}")
            tool_id = tool_call["id"] if "id" in tool_call else str(uuid.uuid4()) ## if tool_id not returned, using uuid
            is_function_call = tool_call["is_function_call"] if "is_function_call" in tool_call else (True if model in [MODEL_SELECTION_GPT4O_ANT] else False)
            if is_function_call:
                tool_name = tool_call["function_name"] if "function_name" in tool_call else (tool_call["name"] if "name" in tool_call else "")
                tool_arguments_str = tool_call["function_arguments"] if "function_arguments" in tool_call else (tool_call["arguments"] if "arguments" in tool_call else {})
                tool_arguments = {}
                try:
                    tool_arguments = json.loads(tool_arguments_str)
                except Exception as e:
                    logging.error(f" Failed to parse json {e}")
                # print (f"Iteration {iterations} DEBUG: Convertion tool_arguments  is {tool_arguments}")
                
                ## tool call input
                message_tool_assistant = tool_call_parameter_wrapper(model, tool_id, tool_name, tool_arguments)
                call_messages.append(message_tool_assistant)
                # print (f"### Agent Loop model {model} message_tool_assistant {message_tool_assistant}")

                ## Add Message tool call execution
                server_name = mcp_tools_dict[tool_name] if tool_name in mcp_tools_dict else ""

                print (f"DEBUG: tool_name {tool_name}, server_name {server_name}, mcp_tools_dict {mcp_tools_dict}")

                tool_name = get_conflict_toolname_original(tool_name, server_name)

                tool_output = run_tool_call(server_name, tool_name, tool_arguments)
                # print (f"Iteration {iterations} DEBUG: agent_loop run_tool_call input server_name {server_name}|tool_name {tool_name}| tool_arguments {tool_arguments}| tool_output {tool_output}")
                ## append message
                status_code = tool_output["status_code"]
                tool_result = tool_output["result"]

                ## Add Message Claude Style
                message_tool_result = tool_call_result_wrapper(model, tool_id, tool_name, tool_result)
                # print (f"### Agent Loop model {model} message_tool_result {message_tool_result}")
                call_messages.append(message_tool_result)

                function_call_result.append({
                    "id": tool_id,
                    "name": tool_name,
                    "input": tool_arguments,
                    "output": tool_output,
                    "status_code": status_code
                })
            else:
                ## end of sequence tool call
                # print (f"Iteration {iterations} DEBUG: End of Sequence Tool Calls")
                loop_end = True
        # print (f"Iteration {iterations} DEBUG: Iteration {iterations} call_messages {call_messages}")

    # print (f"Iteration {iterations} DEBUG: Final call_messages {call_messages}")

    # construct final call result in format
    return function_call_result

def call_llm_tools_function_call_wrapper(model, kwargs):
    """
        Args:
            model: str
            kwargs: dict
        Return:
            dict
    """
    tools = kwargs["tools"] if "tools" in kwargs else []
    messages = kwargs["messages"] if "messages" in kwargs else []
    # logging.info(f"Input call_llm_tools_function_call_wrapper messages {messages}|tools {tools}")

    model_provider = _global_model_provider[model] if model in _global_model_provider else None 
    if model_provider is None:
        logging.error(f"ERROR: call_llm_tools_function_call_wrapper model {model} missing API implementation in _global_model_provider of module model_utils.model_provider")
        return None
    result = model_provider.api_function_call(messages, tools)
    # logging.info(f"Output result {result}")
    tool_call_dict = result[KEY_FUNCTION_CALL] if KEY_FUNCTION_CALL in result else {}
    return tool_call_dict

def call_llm_prediction(query: str, tools: List[Dict], gpt_api) -> Tuple[str, Dict]:
    """
    Call LLM to predict tools and parameters
    
    Args:
        query: User query
        tools: Available tools list
        gpt_api: GPT API instance
        
    Returns:
        Tuple[str, Dict]: (tool name, parameter dictionary)
    """
    # TODO: Implement LLM prediction logic
    pass


def run_tool_call(server_name: str, tool_name: str, function_call_params: Dict) -> Any:
    """
    Running MCP Function Tool Call and Post to Local REST API from open mcp_marketplace
    
    Args:
        server_name: e.g. amap-maps,  the key in mcp config  {"mcpServers": {"amap-maps": {},  "github": {}}}
        tool_name: e.g. maps_weather
        function_call_params: { "city": "New York"}
        
    Returns:
        Any: return MCP results
    """
    try:

        assert isinstance(server_name, str) and server_name is not None
        assert isinstance(tool_name, str) and tool_name is not None
        assert isinstance(function_call_params, Dict) and function_call_params is not None
        # logging.info(f"Running MCP server_name {server_name} Tool {tool_name} Call Params {function_call_params}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                "Content-Type": "application/json"
        }
        url = 'http://127.0.0.1:5000/api/query'
        input_params = {
            "server_id": server_name, 
            "tool_name": tool_name,
            "tool_input": function_call_params
        }
        response = requests.post(url, data=json.dumps(input_params), headers=headers, timeout=5)
        status_code = response.status_code
        result_json = response.json()
        # print (f"DEBUG: run_tool_call response {result_json}")
        output = {
            "status_code": status_code, 
            "result": result_json
        }
        return output
    except Exception as e:
        # return 500 server error code
        # logging.error(f" Failed to run_tool_call mcp server_name {server_name} toolname {tool_name} function_call_params {function_call_params} with error {e}")
        output = {
            "status_code": 500,
            "result": {}
        }
        return output

def check_correctness(pred_tool_result_list: List[Dict], label_result_list: List[Dict]) -> bool:
    """
    Check the correctness of tool calls
    
    Args:
        pred_tool_result_list: format  [{"status_code": 200, "result": Dict}, {"status_code": 500, "result": Dict}]

            {
                "id": tool_id,
                "name": tool_name,
                "input": tool_arguments,
                "output": tool_result,
                "status_code": status_code
            }

        label_result_list: Tool call result list
            
            # input 
            [{
                "id": "1",            
                "name": "playwright_navigate",
                "arguments": {
                  "url": "https://www.wikipedia.org",
                  "browserType": "chromium"
                },
                "step": "1"
            }] 

    Returns:
        List[bool]: Correctness check result list
    """
    label_step = len(label_result_list) if label_result_list is not None else 0
    predict_step = len(pred_tool_result_list) if pred_tool_result_list is not None else 0

    correctness_result = False 

    if (label_step == 1 and predict_step == 1):
        label_result = label_result_list[0]
        pred_tool_result = pred_tool_result_list[0]

        # implementation
        label_tool_name = label_result["name"] if "name" in label_result else ""
        label_result = label_result["output"] if "output" in label_result else {}

        # prediction
        predict_tool_name = pred_tool_result["name"] if "name" in pred_tool_result else ""
        predict_result = pred_tool_result["output"] if "output" in pred_tool_result else {}
        predict_status_code = predict_result["status_code"] if "status_code" in predict_result else 500

        if predict_status_code == 200:
            correctness_result = True
            # if label_tool_name != predict_tool_name:
            #     correctness_result = False
            # else:
            #     # run success
            #     if label_result == predict_result:
            #         correctness_result = True
            #     else:
            #         # sometimes the expected output might differs from the given label due to API change, need to add customized method or AI judgement
            #         tool_call_result_check_func = _global_tool_result_check_func_provider[predict_tool_name] if predict_tool_name in _global_tool_result_check_func_provider else base_compare_result
            #         if tool_call_result_check_func is not None:
            #             correctness_result = tool_call_result_check_func(predict_result, label_result)
            #         print (f"DEBUG: check_correctness tool_name {predict_tool_name} tool_call_result_check_func {tool_call_result_check_func.__name__} correctness_result {correctness_result}")
        else:
            correctness_result = False

    elif (label_step == 1 and predict_step > 1):


        correctness_result = False
    elif (label_step > 1 and predict_step == 1):

        correctness_result = False
    else:
        ## multiple
        correctness_result = False

    # print (f"DEBUG: check_correctness | label_result_list size {label_step} {label_result_list} and |pred_tool_result_list predict_step {predict_step} {pred_tool_result_list}|result {correctness_result}")

    return correctness_result

def evaluate_score(generation: Dict, reference: Tuple) -> bool:
    """
    Evaluate score for a single sample
    
    Args:
        generation: Generated answer
        reference: Reference answer (code, input, output)
        
    Returns:
        bool: Whether passed evaluation
    """
    # TODO: Implement evaluation logic
    pass


def run_benchmark(args):
    """
    Run benchmark test
    
    Data format example (JSON array, each element is an object):
    {
        "query": "How's the weather in Hangzhou, help me check the recent high-speed rail to Hangzhou",
        "ground_truth_label": {
            "node_check_weather": [
                {"tool_name": "baidu_get_weather", "tool_result": "35"}, 
                {"tool_name": "amap_get_weather", "tool_result": "35"}
            ],
            "node_check_schedule": [{"tool_name": "check_schedule", "result": "text"}],
            "path": [("node_check_weather", "node_check_schedule")]
        }
    }
    """
    # Validate evaluation_trial_per_task vs pass_k values
    pass_k_list = [int(k) for k in str(args.pass_k).split(",")]
    max_pass_k = max(pass_k_list)
    evaluation_trial_per_task = args.evaluation_trial_per_task
    if evaluation_trial_per_task < max_pass_k:
        error_msg = f"ERROR: evaluation_trial_per_task ({evaluation_trial_per_task}) must be greater than or equal to the maximum pass@k value ({max_pass_k}). Current pass_k values: {pass_k_list}"
        print(error_msg)
        raise ValueError(error_msg)
    
    print(f"Validation passed: evaluation_trial_per_task={evaluation_trial_per_task}, max_pass_k={max_pass_k}")
    
    # Loading Data from Instances
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    # data_list = data_list[:500] # for debug
    print(f"Loaded {len(data_list)} instances of data files")
    all_results = []

    # Create log record structure
    log_data = {
        "run_info": {
            "input_file": args.input_file,
            "model": args.model,
            "category": args.category,
            "pass_k": args.pass_k,
            "evaluation_trial_per_task": evaluation_trial_per_task,
            "start_time": datetime.datetime.now().isoformat(),
            "total_instances": len(data_list)
        },
        "metrics": [],
        "run_details": []
    }

    num_trails_array = []
    num_pass_array = []
    num_tasks = 0
    for i, data in enumerate(tqdm(data_list, desc="evaluation", unit="instance")):
        num_tasks += 1

        ## preprocess data line
        query = data["query"]
        tools = json.loads(data["tools"]) if isinstance(data["tools"], str) else data["tools"]
        function_call_label = json.loads(data["function_call_label"]) if isinstance(data["function_call_label"], str) else data["function_call_label"]

        mcp_server_tools = data["mcp_tools_dict"] if "mcp_tools_dict" in data else {}
        mcp_server_tools_dict = json.loads(mcp_server_tools) if isinstance(mcp_server_tools, str) else mcp_server_tools

        ## change to parallel
        k_results = []
        task_details = {
            "idx": i,
            "query": query,
            # "tools": tools,
            "function_call_label": function_call_label,
            # "mcp_tools_dict": mcp_server_tools_dict,
            "trials": []
        }
        
        for idx in range(evaluation_trial_per_task):
            # Execute tool call
            function_call_result = agent_loop(query, tools, args.model, mcp_tools_dict=mcp_server_tools_dict)
            # bool result
            if_pass = check_correctness(function_call_result, function_call_label)
            tool_correctness, parameter_correctness = check_ast(
                function_call_result, 
                function_call_label
            )
            k_results.append(if_pass)
            
            # Record detailed information for each trial
            trial_detail = {
                "trial_idx": idx,
                "function_call_result": function_call_result,
                "if_pass": if_pass,
                "tool_correctness": True if tool_correctness == 1 else False,
                "parameter_correctness": True if parameter_correctness == 1 else False
            }
            task_details["trials"].append(trial_detail)

        # 
        num_trails_array.append(evaluation_trial_per_task)
        num_pass_array.append(sum(k_results))
        
        # Calculate pass@k result for this data (pass if any of k trials succeed)
        data_pass = any(k_results)
        all_results.append(data_pass)
        
        # Add task-level summary information
        task_details["k_results"] = k_results
        task_details["data_pass"] = data_pass
        task_details["num_trials"] = evaluation_trial_per_task
        task_details["num_passed"] = sum(k_results)
        
        log_data["run_details"].append(task_details)
    
    # Calculate final metrics
    total_data = len(all_results)
    passed_data = sum(all_results)
    pass_rate = (passed_data / total_data) * 100 if total_data > 0 else 0
    
    # pass_k_list already defined in validation section above

    metrics_list = []
    for k in pass_k_list:
        pass_at_k_arr = estimate_pass_at_k(num_trails_array, num_pass_array, k)          
        pass_at_k = sum(pass_at_k_arr)/len(pass_at_k_arr)
        # print (f"DEBUG: K {k} at pass_at_k {pass_at_k} |Details num_trails_array {num_trails_array} num_pass_array {num_pass_array} pass_at_k_arr {pass_at_k_arr}")
        metric = {
            "category": args.category,
            "model": args.model,
            f"pass@{k}": pass_at_k,
            "num_tasks": num_tasks,
            "num_trials_total": sum(num_trails_array),
            "num_passed_total": sum(num_pass_array)
        }
        metrics_list.append(metric)
        log_data["metrics"].append(metric)

    # Add end time
    log_data["run_info"]["end_time"] = datetime.datetime.now().isoformat()
    
    # Save log file
    save_log_file(log_data, args)
    
    print(f"Final Evaluation: {metrics_list}")
    return metrics_list

def save_log_file(log_data: Dict, args) -> None:
    """
    Save run log to JSON file
    
    Args:
        log_data: Dictionary containing run information
        args: Command line arguments
    """
    try:
        # Create logs directory structure
        logs_dir = os.path.join(os.getcwd(), "logs", args.category)
        os.makedirs(logs_dir, exist_ok=True)
        
        # Generate filename: based on input filename and current time
        input_filename = os.path.basename(args.input_file)
        input_name = os.path.splitext(input_filename)[0]  # Remove extension
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{input_name}_{current_time}.json"
        
        # Complete log file path
        log_file_path = os.path.join(logs_dir, log_filename)
        
        # Save log file
        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"Log file saved to: {log_file_path}")
        
    except Exception as e:
        logging.error(f"Failed to save log file: {e}")

def main():

    ## 1. Run Test of Starting MCP Server amap and test results
    ## Running MCP server_name puppeteer Tool puppeteer_navigate Call Params {'url': 'https://arxiv.org/'} output {'status_code': 200, 'result': {'success': True, 'data': ['Navigated to https://arxiv.org/'], 'error': None}}
    server_name = "puppeteer"
    tool_name = "puppeteer_navigate"
    function_call_params = {
        "url": "https://arxiv.org/"
    }
    output = run_tool_call(server_name, tool_name, function_call_params)
    print (f"Running MCP server_name {server_name} Tool {tool_name} Call Params {function_call_params} output {output}")

if __name__ == '__main__':
    main()
