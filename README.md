# MCPToolBench++: AI Agent MCP Model Context Protocol MCP Tool Use Benchmark

[![MCP Marketplace User Review Rating Badge](https://www.deepnlp.org/api/marketplace/svg?name=mcp-tool-bench/mcptoolbenchpp)](https://www.deepnlp.org/store/ai-agent/benchmark/pub-mcp-tool-bench/mcptoolbenchpp)
[![AI Agent Marketplace DeepNLP](https://www.deepnlp.org/api/ai_agent_marketplace/svg?name=mcp-tool-bench/mcptoolbenchpp)](https://www.deepnlp.org/store/ai-agent/benchmark/pub-mcp-tool-bench/mcptoolbenchpp) 

MCPToolBench++ is a large-scale, multi-domain AI Agent Tool Use Benchmark. As of June 2025, this benchmark includes over 4k+ MCP Servers from more than 45 categories collected from the MCP and GitHub communities. The dataset comprises both single-step and multi-step tool calls across different categories. And we evaluated some SOTA Agent LLMs and RAG-Based Systems. 

Notice: This repo benchmark is still WIP and more domain dataset will be released.


## Performance Leaderboard

|     | Browser |      | File System |      | Search | |
| --- | ------  | ---- | ----| ---- |  --- | ---  |
|     | AST | Pass@1 | AST | Pass@1 |  AST | Pass@1  |
| GPT4o | 0.6524 | 0.2182 | 0.8863 | 0.8232 | 0.5280 | 0.4960 |
| Qwen3 Max | 0.7262  | 0.2749 | 0.9419 | 0.8871 | 0.5240 | 0.3760 |
| Claude Sonnet 3.7 | 0.6503 | 0.1840 | 0.8415 | 0.8183 | 0.4400 | 0.3280 |
| Qwen3 Coder | - | - | - | - | - | - |
| Kimi K2 Instruct | - | - | - | - | - | - |
| Claude Opus 4 | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - |



|     | Map |      | Pay |      | Finance | |
| --- | ------  | ---- | ----| ---- |  --- | ---  |
|     | AST | Pass@1 | AST | Pass@1 |  AST | Pass@1  |
| GPT4o | 0.6120  |  0.3616 | 0.7077 | 0.5742 | 0.7200 | 0.2889 |
| Qwen3 Max | 0.4552 | 0.0984 | 0.6684 | 0.5277 | 0.7511 | 0.2556 |
| Claude Sonnet 3.7 | 0.5820  |  0.2748 | 0.7058 | 0.5574 | 0.7400 | 0.2311 |
| Qwen3 Coder | - | - | - | - | - | - |
| Kimi K2 Instruct | - | - | - | - | - | - |
| Claude Opus 4 | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - |


## Introduction

### 0. Dataset Overview

|  Category  | Number Instance | MCP Tool Count | Avg Tokens/Tool | Total Tokens  |
| ----- | ------  | ----- | ------  | ----- |
| Browser |  187 | 32 |  107.44 | 3.4k |
| File System | 241 | 11 |  143.82 |  1.6k |
| Search |  181 |  5 | 555.6 | 2.8k |
| Map | 500 | 32 | 401.28 | 13k |
| Finance | 90 | 1 | 505.0  | 0.5k |
| Pay | 310 | 6 | 656.5 | 3.9k |
| Total | 1509 | 87 | 288.3 | 25k |


### 1. Browser

The browser subset evaluates models' ability to use the web browser, typical tools include puppeteer_navigate, puppeteer_screenshot,  puppeteer_click, playwright_screenshot, playwright_navigate, etc. Agent models call the tools to nagivate to the URL, visit page, click on buttons, take screenshot of the webpage, etc.

```
Navigate to the Wikipedia website using browser and check its accessibility.
```

#### Setup MCP Servers and API

See [Browser Use MCP Setup](#1-browser-use-mcp-setup) for how to setup and start the servers.

#### Run Dataset

After setup the servers for tool call details, Run below command

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


#### Setup MCP Servers and API
See [File System MCP Setup](#2-file-system-mcp-setup) for how to setup and run MCP servers


#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/file_system/filesystem_0723_demo.json --category filesystem --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/file_system/filesystem_0723_single.json --category filesystem --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


### 3. Search

The search mcp tools helps to search the web given user's query, typical servers and tools include google-web-search, google-image-search, tavily-search, tavily-extract, firecrawl-search, etc.


#### Setup MCP Servers and API
See [Search MCP Setup](#3-search-mcp-setup) for how to setup and run MCP servers


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

#### Setup MCP Servers and API
See [Map MCP Setup](#4-map-mcp-setup) for how to setup and run MCP servers


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

#### Setup MCP Servers and API

The paypal and alipay MCPs are free to use, but you needs to register and setup paypal/alipay sandbox access_key with development account and setup config in mcp-marketplace UI.

See [Pay MCP Setup](#5-pay-mcp-setup) for how to setup and run MCP servers


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

#### Setup MCP Servers and API

See [Finance MCP Setup](#6-finance-mcp-setup) for how to setup and run MCP servers


#### Run Dataset

```
## Test Run 1 instance
python3 run.py --stage tool_call --input_file ./data/finance/finance_single_demo.json --category finance --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

## Run the Dataset
python3 run.py --stage tool_call --input_file ./data/finance/finance_0716_single_v2.json --category finance --model qwen3-max --pass_k 1,3 --evaluation_trial_per_task 5

```


## Detail Tutorial How To Use the Benchmark and Setup Environment


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

Run the <code>browser use</code> dataset using the Qwen3-max dataset

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



## MCP and Environment

### 1. Browser Use MCP Setup


|  Cateogry | MCP Server | Github | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| Browser | puppeteer/puppeteer  | [Github](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer) | puppeteer_navigate,puppeteer_screenshot,puppeteer_click,etc, Visit [mcp marketplace](https://www.deepnlp.org/store/mcp-server/browser/pub-puppeteer/puppeteer) to download tool schema |
| Browser |  executeautomation/mcp-playwright  | [Github](https://github.com/executeautomation/mcp-playwright) | playwright_navigate,playwright_screenshot,etc. Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/mcp-server/pub-executeautomation/mcp-playwright) to download tool schema  |

#### Setup and merge the config

```
cd ./MCPToolBenchPP/mcp
git clone https://github.com/AI-Agent-Hub/mcp-marketplace.git

cd ./mcp/mcp-marketplace/app/mcp_tool_use
uvicorn src.app:app --port 5000
```

Start the App and visit the config files

Open MCP Marketplace Admin By Visit http://localhost:5000/mcp/config/category Directory. 

or 
vim ./mcp/mcp-marketplace/app/mcp_tool_use/data/mcp/config/category/mcp_config_browser.json

```

{
    "mcpServers": {
        "puppeteer": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
        },
        "playwright": {
          "command": "npx",
          "args": ["-y", "@executeautomation/playwright-mcp-server"]
        }
    }
}

```


#### Start Server and Curl if Starts Correctly

Restart the Server 

```
uvicorn src.app:app --port 5000
```

Visit http://localhost:5000/mcp and nable the servers In the Admin Page
On MCP Admin Page, Start the browser servers, including puppeteer, playwright, etc.

![MCP Marketplace Browser](https://raw.githubusercontent.com/mcp-tool-bench/MCPToolBenchPP/refs/heads/main/doc/image_browser_puppeteer.jpg)


Then curl if Rest API is Available


Endpoint: http://127.0.0.1:5000/api/query
```

curl -X POST -H "Content-Type: application/json" -d '{
    "server_id": "puppeteer",
    "tool_name": "puppeteer_navigate",
    "tool_input": {
        "url": "https://arxiv.org/list/cs/new"
    }
}' http://127.0.0.1:5000/api/query
```

Result
```
{"success":true,"data":["Navigated to https://arxiv.org/list/cs/new"],"error":null}

```


### 2 File System Mcp Setup


|  Cateogry | MCP Server | Tools | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| File System | filesystem  | https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem | read_file,read_multiple_files,edit_file,list_directory,etc,Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/file/pub-filesystem/filesystem) |


Create a workspace folder to run local file systems

Please use sub foulder in the MCP UI App to get privilege of folder
Let's say you already clone the mcp_markplace project into your local folder ./MCPToolBenchPP/mcp,
create a temp folder <code>test_project_root</code> to run local file testing 

```
mkdir ./mcp/mcp-marketplace/app/mcp_tool_use/test_project_root

```

workspaceFolder should be a absolute path.e.g. : /path/to/folder/test_project_root


vim ./mcp/mcp-marketplace/app/mcp_tool_use/data/mcp/config/mcp_config.json

```
{
  "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "${workspaceFolder}"
        ]
      }
  }
}

```


Endpoint: http://127.0.0.1:5000/api/query
```
curl -X POST -H "Content-Type: application/json" -d '{
    "server_id": "filesystem",
    "tool_name": "list_directory",
    "tool_input": {
        "path": "./"
    }
}' http://127.0.0.1:5000/api/query
```

Result
```

```

Success:
[
  "[FILE] .DS_Store\n[FILE] .env\n[FILE] .env.example\n[FILE] README.md\n[DIR] data\n[DIR] dev\n[DIR] docs\n[FILE] document.md\n[FILE] log\n[FILE] requirements.txt\n[FILE] run_mcp_tool_use.sh\n[DIR] src\n[DIR] test_project_root\n[DIR] tests\n[DIR] web"
]


### 3. Search MCP Setup

**Note** Search MCP Tools Requires API Key. 

Some Tool such as Google Custom Search API have free quota API calls enough to run the benchmark.


|  Cateogry | MCP Server | Github | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| Search |  tavily/mcp_tavily-mcp | https://github.com/tavily-ai/tavily-mcp  | tavily-search,tavily-extract,tavily-crawl,etc  , Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/mcp-server/pub-tavily-ai/tavily-mcp) |
| Search |  mendableai/firecrawl-mcp-server  | https://github.com/mendableai/firecrawl-mcp-server  |   firecrawl_search,firecrawl_scrape,firecrawl_map,firecrawl_crawl,etc,  Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/file/pub-mendableai/firecrawl-mcp-server) |
| Search |  adenot/mcp-google-search  |  https://github.com/adenot/mcp-google-search | search,read_webpage, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/mcp-server/pub-adenot/mcp-google-search)  |
| Search |  leehanchung/bing-search-mcp  |  https://github.com/leehanchung/bing-search-mcp  | bing_web_search,bing_news_search,bing_image_search , Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/mcp-server/pub-leehanchung/bing-search-mcp)  |
| Search |  brave-search/brave-search  | https://github.com/modelcontextprotocol/servers-archived/tree/main/src/brave-search  |  brave_web_search,brave_local_search, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/ai-agent/mcp-server/pub-brave-search/brave-search)  |


vim ./mcp/mcp-marketplace/app/mcp_tool_use/data/mcp/config/category/mcp_config_search.json

```
{
    "mcpServers": {
        "tavily-mcp": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@latest"],
            "env": {
                "TAVILY_API_KEY": "your-key"
            },
            "disabled": false,
            "autoApprove": []
        },
        "bing-search": {
            "command": "uvx",
            "args": [
                "bing-search-mcp"
            ],
            "env": {
                "BING_API_KEY": "your-bing-api-key"
            }
        },
        "brave-search": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-brave-search"
            ],
            "env": {
                "BRAVE_API_KEY": "your-key"
            }
        },
        "firecrawl-mcp": {
            "command": "npx",
            "args": ["-y", "firecrawl-mcp"],
            "env": {
                "FIRECRAWL_API_KEY": "your-key"
            }
        },
        "google-search": {
                "command": "npx",
                "args": [
                  "-y",
                  "@adenot/mcp-google-search"
                ],
                "env": {
                  "GOOGLE_API_KEY": "your_key",
                  "GOOGLE_SEARCH_ENGINE_ID": "your_key"
                }
        }
    }
}

```



### 4. Map MCP Setup

|  Cateogry | MCP Server | Github | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| Map |  google-map |  -  | maps_direction_bicycling,maps_direction_driving,maps_direction_transit_integrated,etc , Visit more tools at [mcp marketplace](https://deepnlp.org/store/mcp-server/map/pub-google-maps/google-maps) |
| Map |  amap-amap-sse/amap-amap-sse |  -  | maps_direction_bicycling,maps_direction_driving,maps_direction_transit_integrated,etc, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/map/pub-amap-mcp/amap-mcp-%E9%AB%98%E5%BE%B7%E5%9C%B0%E5%9B%BE-mcp) |
| Map |  baidu-map | -  | maps_direction_bicycling,maps_direction_driving,maps_direction_transit_integrated,etc, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/map/pub-baidu-map/baidu-map-mcp-%E7%99%BE%E5%BA%A6%E5%9C%B0%E5%9B%BE-mcp-server) |



### 5. Pay MCP Setup

|  Cateogry | MCP Server | Github | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| Pay |  paypal |  -  |  create_invoice,create_product,etc, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/payment/pub-paypal/paypal) |
| Pay |  alipay |  -  |  create-mobile-alipay-payment,etc, Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/payment/pub-alipay/alipay-mcp-server-%E6%94%AF%E4%BB%98%E5%AE%9D-mcp-server) |


```

```


### 6. Finance MCP Setup


|  Cateogry | MCP Server | Tools | Config and Tool Schema Files Download  |
| ---- | ---- | ---- | ---- |
| Finance |  finance-agent-mcp-server  |  https://github.com/AI-Hub-Admin/finance-agent-mcp-server  | get_stock_price_global_market, etc. Visit more tools at [mcp marketplace](https://www.deepnlp.org/store/mcp-server/finance/pub-ai-hub-admin/finance-agent-mcp-server) |
| Finance |  yahoo-finance |  -  |  -  | - |


```
{
    "mcpServers": {
        "finance-agent-mcp-server": {
            "command": "uv",
            "args": ["--directory", "./finance-agent-mcp-server/src/finance-agent-mcp-server", "run", "server.py"]
        }
}
```


