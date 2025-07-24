# MCPToolBench++: AI Agent MCP Model Context Protocol MCP Tool Use Benchmark

[![MCP Marketplace User Review Rating Badge](https://www.deepnlp.org/api/marketplace/svg?name=mcp-tool-bench/mcptoolbenchpp)](https://www.deepnlp.org/store/ai-agent/benchmark/pub-mcp-tool-bench/mcptoolbenchpp)
[![AI Agent Marketplace DeepNLP](https://www.deepnlp.org/api/ai_agent_marketplace/svg?name=mcp-tool-bench/mcptoolbenchpp)](https://www.deepnlp.org/store/ai-agent/benchmark/pub-mcp-tool-bench/mcptoolbenchpp) 

MCPToolBench++ is a large-scale, multi-domain AI Agent Tool Use Benchmark. As of June 2025, this benchmark includes over 4k+ MCP Servers from more than 45 categories collected from the MCP and GitHub communities. The dataset comprises both single-step and multi-step tool calls across different categories. And we evaluated some SOTA Agent LLMs and RAG-Based Systems. 

Notice: This repo benchmark is still WIP and more domain dataset will be released.


## Performance Leaderboard

|     | Browser |      | File System |      | Search | |
| --- | ------  | ---- | ----| ---- |  --- | ---  |
|     | AST | Pass@1 | AST | Pass@1 |  AST | Pass@1  |
| Claude Opus 4 | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - |
| GPT4o | - | - | 0.8863 | 0.8232 | - | - |
| Claude Sonnet 3.7| - | - | 0.8415 | 0.8183 | - | - |
| Qwen3 Max | - | - | 0.9419 | 0.8871 | - | - |
| Qwen3 Coder | - | - | - | - | - | - |
| Kimi K2 Instruct | - | - | - | - | - | - |


|     | Map |      | Pay |      | Finance | |
| --- | ------  | ---- | ----| ---- |  --- | ---  |
|     | AST | Pass@1 | AST | Pass@1 |  AST | Pass@1  |
| Claude Opus 4 | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - |
| GPT4o | - | - | 0.7077 | 0.5742 | - | - |
| Claude Sonnet 3.7| - | - | 0.7058 | 0.5574 | - | - |
| Qwen3 Max | - | - | 0.6684 | 0.5277 | - | - |
| Qwen3 Coder | - | - | - | - | - | - |
| Kimi K2 Instruct | - | - | - | - | - | - |


## Introduction

### 1. Browser

The browser subset evaluates models' ability to use the web browser, typical tools include puppeteer_navigate, puppeteer_screenshot,  puppeteer_click, playwright_screenshot, playwright_navigate, etc. Agent models call the tools to nagivate to the URL, visit page, click on buttons, take screenshot of the webpage, etc.


```
Navigate to the Wikipedia website using the Chromium browser and check its accessibility.
```

#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/browser/browser_single_demo.json --category browser --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/browser/browser_0713_single.json --category browser --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


### 2. File System

The file system mcp helps to manage your local file and directories, typical tools include: read_file/edit_File/list_directory_with_sizes/etc.

```
Read the contents of the files located at ./test_project_root/src/main.py and ./test_project_root/docs/README.md at the same time.

Provide a recursive tree view of the files and directories located at ./test_project_root/src.
```


#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/file_system/filesystem_0723_demo.json --category filesystem --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/file_system/filesystem_0723_single.json --category filesystem --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


### 3. Search

The search mcp tools helps to search the web given user's query, typical servers and tools include google-web-search, google-image-search, tavily-search, tavily-extract, firecrawl-search, etc.


```
Find latest AI LLM and Agents related news on the web
```


#### Run Dataset

```

```


### 4. Map


```
# english
What is the current weather in Tokyo and the weather forecast for the next 5 days?
Find popular Japanese restaurants in Houston.

# french
¿Cuál es la mejor ruta para ir en bicicleta desde Tokio hasta la Torre de Tokio?
# russian
Каковы координаты адреса Санкт-Петербург, Невский проспект, 1?

```

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/map/map_0717_single_demo.json --category map --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/map/map_0717_single_multi_lang_500.json --category map --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


### 5. Pay

The pay subdataset evaluates pay related MCP servers(paypal/alipay/etc), typical tools include create_invoice, create_products, etc.

Data Instance
```
Create an invoice for Tech Solutions Inc. for a Consultation Service costing 150.00 USD.
```

#### Setup

The paypal and alipay MCPs are free to use, but you needs to register and setup paypal/alipay sandbox access_key with development account and setup config in mcp-marketplace UI.

#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/pay/pay_0723_single_demo.json --category pay --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/pay/pay_0723_single.json --category pay --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```



### 6. Finance

Data Instance
```
What is the current stock price of Tesla in the US market?
What is the current stock price and market capitalization of Shell in the London Stock Exchange market?
```


#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/finance/finance_single_demo.json --category finance --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/finance/finance_0716_single_v2.json --category finance --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


## Detail Tutorial How To Use the Benchmark

### 0. Setup

Clone the repo https://github.com/mcp-tool-bench/MCPToolBenchPP

```
## dataset
git clone https://github.com/mcp-tool-bench/MCPToolBenchPP

## clone the mcp client to execute tool call
cd ./mcp
## path: ./mcp/mcp-marketplace
git clone https://github.com/AI-Agent-Hub/mcp-marketplace
```

#### Setup Env Keys
Edit .env file
```
cd ./MCPToolBenchPP
vim .env
```

```txt
QWEN_API_KEY=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
```

#### Setup Client MCP Marketplace Admin and start Servers

You need to install requirements and follow the steps in https://github.com/AI-Agent-Hub/mcp-marketplace

```
cd ./mcp/mcp-marketplace/app/mcp_tool_use
uvicorn src.app:app --port 5000
```

Change Configuration start all servers from mcp_config.json when starting the server
```
# edit ./mcp/mcp-marketplace/app/mcp_tool_use/src/constants.py

MCP_INIT_AUTO_ENABLE=True

Manage the MCP Configs Started at ./mcp/mcp-marketplace/app/mcp_tool_use/data/mcp/config/mcp_config.json
Visit http://127.0.0.1:5000/mcp to see started servers and edit config 
```

### 1. Run Evaluation 

Run the <code>browser user</code> user dataset using the Qwen3-max dataset

####  Start Open MCP Marketplace Client to Execute Tool Call

```
cd ./mcp/mcp-marketplace/app/mcp_tool_use
uvicorn src.app:app --port 5000
```

```txt
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/browser/browser_single_demo.json --category browser --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5


## Browser Use Dataset
python3 run.py --stage tool_call --input_file ./data/browser/browser_0713_single_500.json --category browser --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5


```

Output
```
Output of browser_single_demo.json 1 task
# Log file saved to: ./mcp-tool-bench/logs/browser/browser_single_demo_xxxx_xxxx.json
# Final Evaluation: [{'category': 'browser', 'model': 'qwen3-max', 'pass@1': 1.0, 'num_tasks': 1, 'num_trials_total': 1, 'num_passed_total': 1}]
```


### 2. Data Example 

This illustrate the schema of one MCP Tool Use Benchmark task.

```
Query: Navigate to the Wikipedia website using the Chromium browser and check its accessibility.
Assistant:  Run MCP Tools  playwright_navigate(url = "https://www.wikipedia.org", "browserType": "chromium")
```

```
[{
    "uuid": "0b1be01a-a542-4f54-8cfc-017760c03d72",
    "category": "browser",
    "call_type": "single",
    "tools": [{
            "name": "playwright_navigate",
            "description": "Navigate to a URL",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to the website specified"
                    },
                    "...": {}
                },
                "required": ["url"]
            }
        },
        {
            "....": {}
        }
    ],
    "mcp_tools_dict": {
        "playwright": ["start_codegen_session", "end_codegen_session", "get_codegen_session", "clear_codegen_session", "playwright_navigate", "playwright_screenshot", "playwright_click", "playwright_iframe_click", "playwright_iframe_fill", "playwright_fill", "playwright_select", "playwright_hover", "playwright_evaluate", "playwright_console_logs", "playwright_close", "playwright_get", "playwright_post", "playwright_put", "playwright_patch", "playwright_delete", "playwright_expect_response", "playwright_assert_response", "playwright_custom_user_agent", "playwright_get_visible_text", "playwright_get_visible_html", "playwright_go_back", "playwright_go_forward", "playwright_drag", "playwright_press_key", "playwright_save_as_pdf", "playwright_click_and_switch_tab"],
        "puppeteer": ["puppeteer_navigate", "puppeteer_screenshot", "puppeteer_click", "puppeteer_fill", "puppeteer_select", "puppeteer_hover", "puppeteer_evaluate"]
    },
    "query": "Navigate to the Wikipedia website using the Chromium browser and check its accessibility.",
    "function_call_label": [{
        "name": "playwright_navigate",
        "step": "1",
        "id": "1",
        "mcp_server": "playwright",
        "similar_tools": [{
            "name": "puppeteer_navigate",
            "mcp_server": "puppeteer"
        }],
        "input": {
            "url": "https://www.wikipedia.org",
            "browserType": "chromium"
        },
        "output": {
            "status_code": 200,
            "result": {}
        }
    }]
}]
```
