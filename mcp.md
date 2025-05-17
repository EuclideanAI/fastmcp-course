# MCP Course: Building AI-Native Applications with Model Context Protocol

## Introduction (0:00 - 1:30)

Hey everyone! Welcome to this course on the Model Context Protocol, or MCP. I'm excited to dive into this with you today because MCP is revolutionizing how we build AI applications. Whether you're a developer who's been working with LLMs for a while or you're just getting started, MCP is something you'll want to understand.

In the next hour, we'll cover what MCP is, why it matters, how it works under the hood, and I'll walk you through building your own MCP server. By the end of this course, you'll have a practical understanding of how to implement MCP in your own projects.

## Quick Demo (1:30 - 10:00)

Before I get into the details, let me show you MCP in action with a real-world productivity example that demonstrates its power in a development workflow.

[Screen shows VS Code with GitHub Copilot installed]

For this demo, I'll be using VS Code with GitHub Copilot, which has been enhanced with MCP capabilities to connect directly to Atlassian's ecosystem. This integration allows the AI to not only understand our prompts but also interact with our company's knowledge base and workflow tools.

Let's imagine we're a product manager who needs to create a PRD (Product Requirements Document) for a new AI-powered baby tracker app. Traditionally, we'd have to write this document from scratch, referencing various sources and then manually upload it to our company wiki. With MCP, the workflow becomes much more streamlined.

[Demo starts with opening the GitHub Copilot chat interface in VS Code]

First, I'll open GitHub Copilot's chat interface in VS Code. 

Let me type a prompt to get started:

[Typing into the Copilot chat interface]

"I need to create a PRD for an AI-powered baby tracker app. The app should help parents track feeding times, sleep patterns, nappy changes, and growth milestones. It should use AI to provide insights and predictions about the baby's development. The target audience is first-time parents, and we want to emphasize ease of use and peace of mind."

Now watch what happens when I send this prompt.

[Sending the prompt and waiting for response]

[Show Copilot generating a structured PRD]

Look at that! Copilot has generated a complete PRD for our AI Baby Tracker. The document includes:

- Executive Summary
- Problem Statement
- Target Audience
- Solution Overview
- Feature Requirements
- Technical Requirements
- Success Metrics
- Timeline
- Resources Needed

Now for the really powerful part - let's see if we can post this directly to Confluence, our company wiki.

[Typing into the Copilot chat interface]

"This looks great! Can you post this PRD to our Confluence space under 'Software development' with the title 'AI Baby Tracker - PRD'?"

[Send the message]

Watch what happens now.

[Screen shows Copilot processing the request]

Copilot is using MCP to communicate with our Atlassian Confluence instance. It's not just generating text - it's performing an action by creating a new page in our wiki with all the formatted content.

It's formatted exactly according to our company's standard PRD template, which it accessed through the MCP connection to our Atlassian environment. Without MCP, I would have had to explicitly instruct the AI about our document format or manually format it afterward.

[Screen shows confirmation from Copilot with a link to the newly created Confluence page]

There we go! Copilot has successfully created a new page in our Confluence space with the complete PRD. Let me refresh and show you.

[Clicks the link, opening the Confluence page]

As you can see, the entire PRD has been posted to Confluence with proper formatting, headings, bullet points, and even our company's styling. The document is now immediately available to our entire team.

This is the power of MCP – it extends beyond simple text generation to enable AI models to understand structured data (like our company's documentation standards) and to take actions (like creating a Confluence page). The AI isn't just responding with text; it's integrated into our tools and workflows.

Now that you've seen what it can do, let's talk about what MCP actually is.

## What's MCP (10:00 - 20:00)

So what exactly is MCP? MCP stands for Model Context Protocol, and it's an open protocol for enabling AI models to natively understand structured data and connect to various services.

[Screen shows Image 1 - The expanded MCP architecture with USB hub metaphor]

This diagram gives us a more visual way to understand MCP. Think of it like a USB hub for AI applications - a universal connector that works regardless of which LLM or tools you're using. Your MCP client might be interfacing with multiple servers simultaneously, each providing access to different services like Atlassian Confluence, Jira, Slack, Gmail, or Google Calendar.

At its core, MCP is a standardized way to represent and exchange data between applications and AI models. It moves beyond the traditional approach of treating everything as plain text strings.


## Why MCP Matters (20:00 - 30:00)

So we've seen what MCP is, but why should you care? How does it change the AI development landscape?

Imagine you're running GitHub Copilot in Agent Mode, or using Anthropic's Claude Desktop. You want your agent to fetch data from GitHub, access your local file systems, and maybe kick off a CI/CD build via github actions—all in one conversational session. In the pre-MCP world, each of those integrations comes with its own challenges:

* Different API specifications (OpenAPI vs GraphQL vs custom REST)
* Various authentication schemes (Bearer token, Basic Auth, API key)
* Unique documentation, error-handling quirks, rate limits...

Your prompts—and your code—quickly become a tangle of bespoke logic. As new LLMs, new tools, and new authentication methods emerge, every single integration is a fresh headache.

What if there were a universal "USB-C port" for AI applications—one connector that just works, regardless of your choice of LLM or your toolset? That's exactly what MCP promises:

* **Pre-built integrations** your model can "plug into" whatever services you have alredy got connection to
* **Vendor-agnostic flexibility** to swap LLMs without rewriting your toolchain
* **Security best practices** baked in, so you don't have to reinvent authentication every time

## How MCP works (20:00 - 30:00)

[Screen shows Image 2 - The MCP architecture diagram with client-host-server structure]

Let's look at the general architecture of MCP as shown in this diagram. MCP follows a client-host-server architecture that provides a clean separation of concerns:

- **MCP Hosts**: These are programs like Claude Desktop, IDEs like VS Code, Cursor, Windsurf (you name it) that want to access data through MCP
- **MCP Clients**: Protocol clients that maintain 1:1 connections with servers
- **MCP Servers**: Lightweight programs that each expose specific capabilities through the standardized protocol - things like tools, resources, and prompts
- **Local Data Sources**: Your computer's files, databases, and services that MCP servers can securely access
- **Remote Services**: External systems available over the internet that MCP servers can connect to, in our case Atlassian Confluence

Let's break down some key concepts:

First, what's a protocol? In computing, a protocol is simply a set of rules that allow different systems to communicate with each other. Think about HTTP, which is the protocol that powers the web. MCP is like HTTP, but specifically designed for AI model powered applications.

### Transport Layer

The transport layer handles the actual communication between clients and servers. MCP supports two transport mechanisms:

**Stdio transport**
- Uses standard input/output for communication
- Ideal for local processes

**HTTP with SSE transport**
- Uses Server-Sent Events for server-to-client messages (e.g. the responses that get sent back from the LLM provider like OpenAI, Anthropic)
- HTTP POST for client-to-server messages

All transports use JSON-RPC 2.0 to exchange messages. 


## Building Your Own MCP Server (40:00 - 55:00)

Now, let's get hands-on and build an MCP server. This will help solidify the concepts we've discussed and give you practical experience with MCP.

We'll build a simple MCP server that can handle basic context types and interface with an LLM. For this demo, I'll use Python, but the concepts apply to any language.

First, let's set up our environment:

```bash
# Create a virtual environment
python -m venv mcp-demo
source mcp-demo/bin/activate  # On Windows: mcp-demo\Scripts\activate

# Install required packages
pip install fastapi uvicorn pydantic python-multipart requests
# If you're using OpenAI
pip install openai
# If you're using a different provider, install their SDK
```

Now, let's create our MCP server. We'll use FastAPI for the HTTP server:

```python
# mcp_server.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import requests
import json
import base64
import os
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define our data models based on the MCP spec
class ContextBlock(BaseModel):
    id: str
    type: str
    data: Any = None
    ref: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str
    context: Optional[List[ContextBlock]] = None

class MCPRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-4"

class MCPResponse(BaseModel):
    role: str
    content: str
    context: Optional[List[ContextBlock]] = []

# Helper function to resolve references
def resolve_reference(ref: str) -> Any:
    response = requests.get(ref)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to resolve reference: {ref}")
    
    content_type = response.headers.get("Content-Type", "")
    if content_type.startswith("application/json"):
        return response.json()
    elif content_type.startswith("text/"):
        return response.text
    else:
        # For binary data, encode as base64
        return base64.b64encode(response.content).decode("utf-8")

@app.post("/generate")
async def generate(request: MCPRequest):
    # Process the request
    processed_messages = []
    
    for message in request.messages:
        processed_context = []
        
        if message.context:
            for block in message.context:
                # If there's a reference, resolve it
                if block.ref and not block.data:
                    block.data = resolve_reference(block.ref)
                
                processed_context.append(block)
        
        # Add the processed message
        processed_message = {
            "role": message.role,
            "content": message.content
        }
        
        # Format the context blocks for the model
        if processed_context:
            # This is where we'd format the context blocks for the specific model
            # For now, we'll just include them as a formatted string in the content
            context_str = "\n\n--- CONTEXT BLOCKS ---\n\n"
            for block in processed_context:
                context_str += f"BLOCK ID: {block.id}\n"
                context_str += f"TYPE: {block.type}\n"
                context_str += f"DATA: {json.dumps(block.data, indent=2)}\n\n"
            
            processed_message["content"] = message.content + context_str
        
        processed_messages.append(processed_message)
    
    # Call the AI model
    response = client.chat.completions.create(
        model=request.model,
        messages=processed_messages
    )
    
    # Format the response according to MCP
    return MCPResponse(
        role="assistant",
        content=response.choices[0].message.content
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

[Screen shows coding the above in VS Code]

Let's break down what this code is doing:

1. We define the data models for MCP requests and responses using Pydantic.
2. We implement a function to resolve references, which fetches content from URLs.
3. Our main endpoint processes incoming MCP requests by:
   - Resolving any references in context blocks
   - Formatting the context blocks in a way the model can understand
   - Calling the AI model with the processed messages
   - Returning the response in MCP format

This is a simplified implementation, but it demonstrates the core concepts. In a production environment, you'd want to add:

- Better error handling
- Authentication and rate limiting
- Caching for resolved references
- Support for more context types
- More sophisticated techniques for passing context to the model

Now, let's run our server:

```bash
python mcp_server.py
```

And in a separate terminal, let's test it with a simple request:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Analyze this data and tell me the average value:",
        "context": [
          {
            "id": "data1",
            "type": "application/json",
            "data": {"values": [10, 20, 30, 40, 50]}
          }
        ]
      }
    ],
    "model": "gpt-4"
  }'
```

[Screen shows running the server and sending the request]

Great! Now we have a basic MCP server running. Let's enhance it to support a few more context types, such as CSV data and images.

For CSV data, we'll add a function to parse CSV into a structured format:

```python
import csv
from io import StringIO

def parse_csv(csv_data: str) -> List[Dict[str, str]]:
    reader = csv.DictReader(StringIO(csv_data))
    return list(reader)

# Then in our endpoint:
if block.type == "text/csv" and isinstance(block.data, str):
    # Parse CSV into structured data
    block.data = parse_csv(block.data)
```

[Screen shows adding this code]

For images, we'll need to handle base64-encoded data:

```python
if block.type.startswith("image/") and isinstance(block.data, str):
    # For images, we'll leave them as base64 but might need to 
    # add a prefix for some models
    if not block.data.startswith("data:"):
        block.data = f"data:{block.type};base64,{block.data}"
```

[Screen shows adding this code]

Now let's enhance our MCP client to make it easier to work with:

```python
# mcp_client.py
import requests
import json
import base64
from typing import List, Dict, Any, Optional

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
    
    def generate(self, prompt: str, context: List[Dict[str, Any]] = None, model: str = "gpt-4"):
        """
        Generate a response using the MCP server.
        
        Args:
            prompt: The text prompt to send
            context: A list of context blocks
            model: The model to use
            
        Returns:
            The response from the model
        """
        request_data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "context": context or []
                }
            ],
            "model": model
        }
        
        response = requests.post(
            f"{self.server_url}/generate",
            json=request_data
        )
        
        if response.status_code != 200:
            raise Exception(f"Error from MCP server: {response.text}")
        
        return response.json()
    
    def add_text_context(self, context_list: List[Dict[str, Any]], id: str, text: str) -> List[Dict[str, Any]]:
        """Add a text context block"""
        context_list.append({
            "id": id,
            "type": "text/plain",
            "data": text
        })
        return context_list
    
    def add_json_context(self, context_list: List[Dict[str, Any]], id: str, json_data: Any) -> List[Dict[str, Any]]:
        """Add a JSON context block"""
        context_list.append({
            "id": id,
            "type": "application/json",
            "data": json_data
        })
        return context_list
    
    def add_image_context(self, context_list: List[Dict[str, Any]], id: str, image_path: str) -> List[Dict[str, Any]]:
        """Add an image context block from a file"""
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        # Determine image type from file extension
        image_type = "image/jpeg"  # Default
        if image_path.lower().endswith(".png"):
            image_type = "image/png"
        elif image_path.lower().endswith(".gif"):
            image_type = "image/gif"
        
        context_list.append({
            "id": id,
            "type": image_type,
            "data": image_data
        })
        return context_list
    
    def add_ref_context(self, context_list: List[Dict[str, Any]], id: str, type: str, ref: str) -> List[Dict[str, Any]]:
        """Add a reference context block"""
        context_list.append({
            "id": id,
            "type": type,
            "ref": ref
        })
        return context_list
```

[Screen shows coding this client]

Now let's use our client to send a more complex request:

```python
# example_usage.py
from mcp_client import MCPClient

# Create an MCP client
client = MCPClient("http://localhost:8000")

# Create some context
context = []
client.add_json_context(context, "user_data", {
    "users": [
        {"name": "Alice", "age": 28, "role": "Engineer"},
        {"name": "Bob", "age": 34, "role": "Designer"},
        {"name": "Charlie", "age": 42, "role": "Manager"}
    ]
})

# Add a CSV context block
csv_data = """name,sales,region
John,120,North
Sarah,150,South
Mike,90,East
Lisa,200,West"""
client.add_text_context(context, "sales_data", csv_data)

# Generate a response
response = client.generate(
    "Analyze the user data and sales data. Who has the highest sales?",
    context=context
)

print(json.dumps(response, indent=2))
```

[Screen shows running this example]

This gives you a basic implementation of an MCP server and client. In a real-world scenario, you'd want to:

1. Use a more sophisticated approach to pass structured data to the model
2. Add support for more context types
3. Implement proper authentication and error handling
4. Add caching and performance optimizations

The important thing is that you understand the core concepts:

- MCP is about preserving the structure of your data when communicating with models
- An MCP server acts as a bridge between your application and the model
- The server is responsible for resolving references and formatting data for the model
- The client makes it easy to work with structured data in your application

Let's wrap up with some best practices and advanced topics.

## Advanced Topics and Best Practices (55:00 - 58:30)

Before we conclude, let's touch on some advanced topics and best practices for working with MCP:

**1. Context Type Handling**

Different models may have different capabilities when it comes to handling various context types. When building an MCP server, it's important to:

- Document which context types are supported
- Have fallback mechanisms for unsupported types
- Consider content negotiation for different representations of the same data

**2. Security Considerations**

When working with MCP, keep these security aspects in mind:

- References can expose your application to server-side request forgery (SSRF) attacks
- Validate and sanitize all input data
- Use authentication and authorization for your MCP server
- Be cautious about sensitive data in context blocks

**3. Performance Optimization**

MCP can handle large data sets, but you should still be mindful of performance:

- Implement caching for resolved references
- Consider pagination or streaming for very large datasets
- Use compression when appropriate
- Monitor token usage and optimize accordingly

**4. Integration with Existing Systems**

MCP can be integrated with various systems:

- Database connectors that format query results as context blocks
- File system adapters for working with local files
- API clients that convert responses to context blocks
- Vector databases for retrieval-augmented generation

**5. Advanced Context Types**

Beyond the basic types we've covered, you can work with specialized context types:

- Semantic types for domain-specific data
- Executable code blocks that can be evaluated
- Interactive elements that update based on user input
- Multi-modal context that combines different types

## Conclusion (58:30 - 60:00)

Today, we've covered the Model Context Protocol (MCP) from the ground up:

- We started with a demo showing what MCP can do
- We explored what MCP is and how it differs from traditional approaches
- We discussed why MCP matters and the benefits it brings
- We delved into how MCP works under the hood
- We built our own MCP server and client

MCP represents a significant shift in how we interact with AI models. By preserving the semantic structure of our data, we can build more powerful, efficient, and maintainable AI applications.

As you start implementing MCP in your own projects, remember these key takeaways:

1. MCP is about structure, not just content
2. The protocol is open and designed to work across different models
3. It simplifies application development by reducing prompt engineering
4. It improves model performance and reduces token usage
5. You can start small and gradually adopt more advanced features

The MCP ecosystem is still evolving, and there's a lot of room for innovation. I encourage you to explore the official documentation at modelcontextprotocol.io and contribute to the community.

Thanks for joining me on this journey through MCP. I hope you feel equipped to start using it in your own projects. Feel free to reach out with any questions, and happy coding!

[End Credits]