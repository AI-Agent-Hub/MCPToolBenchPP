# MCPToolBench++: AI Agent MCP Model Context Protocol MCP Tool Use Benchmark

[![MCP Marketplace User Review Rating Badge](https://www.deepnlp.org/api/marketplace/svg?name=mcp-tool-bench/mcptoolbenchpp)](https://www.deepnlp.org/store/ai-agent/benchmark/pub-mcp-tool-bench/mcptoolbenchpp)

MCPToolBench++ is a large-scale, multi-domain AI Agent Tool Use Benchmark. As of June 2025, this benchmark includes over 4k+ MCP Servers from more than 45 categories collected from the MCP and GitHub communities. The dataset comprises both single-step and multi-step tool calls across different categories. And we evaluated some SOTA Agent LLMs and RAG-Based Systems. 

Notice: This repo benchmark is still WIP and more domain dataset will be released.


## Performance Leaderboard

|     | Browser |      | Map |      | Search | |
| --- | ------  | ---- | ----| ---- |  --- | ---  |
|     | AST | Pass@1 | AST | Pass@1 |  AST | Pass@1  |
| Claude Opus 4 | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - |
| GPT4o | - | - | - | - | - | - |
| Claude Sonnet 3.7| - | - | - | - | - | - |
| Qwen3 Max | - | - | - | - | - | - |
| Qwen2.5 Max | - | - | - | - | - | - |


## Use the Benchmark

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
