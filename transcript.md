Hey everyone, welcome to the MCP From Zero to Hero series. Before we get into the nitty gritty of the full course, I want to kick things off with a real-time demo so you can see MCP working in practice.

Alright, let's jump right in.

Imagine I'm a product manager and I type: "I need to create a PRD (Product Requirement Document) — for an AI-powered baby tracker app. The app should help parents track feeding times, sleep patterns, nappy changes, and growth milestones. It should use AI to provide insights and predictions about the baby's development. The target audience is first-time parents, and we want to emphasize ease of use and peace of mind."

As soon as I submit this request, you’ll notice the agent immediately detects the available tools from the Atlassian MCP server. It then starts generating a PRD in a `PRD.md` file. In just a few seconds, we have a comprehensive product requirement document for our baby tracker app.

But that’s not all. Let’s take it a step further. Suppose I ask the AI, "Can you refer to the software development template available in my company's confluence workspace?" The agent will connect to our Atlassian account, locate the relevant product requirement template, and use it as a reference.

Next, The agent triggers a tool from the Atlassian MCP server called Conference Search. It searches the Conference workspace for a few pages relevant to my query, along with their associated metadata. Then, it runs another tool called 'get page' to fetch the full content.

After a brief moment, the agent confirms: "I have successfully created a new Confluence page for your Baby Tracker app. Here’s what I’ve included." If we refresh our Confluence workspace, we’ll see a new page titled "Product Requirements – AI Powered Baby Tracker," complete with objectives, problem statements, target audience, user personas, and success metrics.

What’s especially impressive is that the agent formats tables and sections to match the Confluence template—not just plain markdown. It converts the draft content to align perfectly with the company’s formatting standards.

---

Now, you have seen what's possible. Here’s what we’ll cover in today’s episode:

First, I’ll introduce what MCP is, why it matters, and highlight its key features and benefits.

After that, we’ll set up your development environment together and create your very first MCP server. I’ll explain the core building blocks of MCP: Tools, Resources, Prompts, and Context.

This is a hands-on course, and we’ll work through four practical projects together:

**Project 1:** You’ll build your own Confluence MCP server from scratch, step by step. By the end, you’ll have a production-ready project ready to deploy. I’ll also show you how to integrate your MCP server with both VS Code Copilot and Claude Desktop.

**Project 2:** We’ll explore the main communication transports: standard I/O, SSE (Server-Sent Events), and the latest Streamable HTTP. We’ll also cover authentication for remote servers, important security considerations, and how to deploy a remote server.

**Project 3:** We’ll dive into advanced topics, including how to mount MCP onto an existing FastAPI project, and explain how sampling and proxy servers work.

**Project 4:** You’ll build your own MCP client and explore the details of communication between the MCP client and MCP server.

Without further ado, let’s get started with the introduction!

MCP stands for Model Context Protocol. It's a standardized way for AI models to communicate with various tools and services. Think of it like a universal USB-C connector for AI applications—one standard that works regardless of which AI model or tools you're using.

Just like USB-C lets you use the same cable to connect different devices, MCP makes your AI integrations portable. You can easily swap out one AI model or client for another without having to rewrite all your code.

This modularity means you spend less time on custom integrations and more time building features that matter.And because MCP is a standard, it means everyone integrates with large language models (LLMs) in the same way. Instead of writing custom, one-off code for each new model or tool.

Plus, MCP helps future-proof your projects. As new AI models and tools emerge, you can plug them into your existing setup with minimal changes—just like plugging a new device into a USB-C hub. This flexibility and simplicity are what make MCP so powerful.

Let’s take a moment to explain how MCP works, especially in the context of one of the biggest recent advancements in AI: function calling.

Function calling is a breakthrough that’s enabled large language models (LLMs) to use tools and APIs—much like how humans use tools to extend their abilities. In human history, one key difference between us and other primates is our ability to understand and use tools. The same principle now applies to LLMs.

Here’s the basic idea: In programming, you define functions or methods that perform specific tasks. With function calling, you can provide these function definitions to an LLM. When you send a query, the LLM decides whether it can answer directly or if it needs to use a tool (i.e., call a function). If a function call is needed, the LLM returns an action indicating which function to call and with what parameters. The actual function (or tool/API) is then invoked by your application. The result is passed back to the LLM, which uses it to generate the final response for the user.

While function calling is powerful, it often requires custom code for every new tool, API, or authentication method, and can become complex as you scale.

This is where MCP comes in. MCP standardizes how tools are defined and accessed by LLMs. Instead of writing custom integration code for each new tool or API, you configure tools on an MCP server. Each MCP server can represent a service provider with a collection of APIs. The LLM simply decides when to use a tool; the MCP server handles the rest.

This approach means you don’t have to reinvent the wheel every time you build a new AI application. You just need an MCP client that can talk to an LLM or multiple LLMs and handle responses, while the heavy lifting is managed by the MCP server and service providers.

The portability and extensibility of MCP have been clearly demonstrated in just the last six months since its creation in November 2024. Thousands of MCP servers have already been created and shared across the internet. Several third-party MCP registries now host more than 10,000 MCP servers, covering a wide range of use cases—from data and file systems, development tools, web and browser automation, productivity, and communication.

There are also official integrations available. If you check Anthropic’s official GitHub repository, you’ll find a number of service providers that already offer official MCP servers.

OK, now it's time to get our hands dirty! There are no prerequisites for these sessions, and you don't need to be a Python expert to create an MCP server. There are just two things we need to know before we can start building.

The first is `uv`, a Python package manager. We'll use `uv` to install all our dependency packages. The second is FastMCP. You can visit its website to learn more about what FastMCP is. The name is inspired by a very popular python backend package called FastAPI — FastMCP provides a high-level interface library built on top of the original Python MCP SDK. The benefit is that it's fast to build with, simplifies the development process, reduces boilerplate code, and is very Pythonic and beginner-friendly.

To install UV is pretty straightforward. Just follow the instructions on the UV documentation—it works for both macOS and Windows users. There is just one simple command you need to run, depending on your operating system. Once UV is installed, you don’t need to manually download Python yourself. UV can automatically install and manage different Python versions for you. It’s a fully managed solution that provides an excellent way to handle Python versions and dependencies across multiple projects.

Let's get started:

1. First, use `uv init` to create a new project.
2. Then, run `uv add fastmcp` to install Fast MCP and all its dependencies. This only takes a few seconds.
3. If you're curious, you can check the `uv.lock` file to see all the dependency information.

After installation, you'll want to activate your virtual environment. Once you're inside the `.venv` environment, you can check the Fast MCP version by typing `fastmcp version`. This will display the current Fast MCP version as well as your Python version.

Now, let's start with a simple "Hello World" server. Before we do that, let's rename our `main.py` file to `server.py`. You can remove the main function, and then start by importing the Fast MCP class:

```python
from fast_mcp import FastMCP

mcp = FastMCP(name="My MCP Server")
```

After you've created the FastMCP class instance, let's add a simple tool that performs the addition of two numbers. You can use the `@mcp.tool` decorator to define the tool, specifying the input and output types.

Next, let's create a resource. Refer to the Fast MCP documentation to see how to define a resource using the `@resource` decorator. For example, you can copy the sample config data resource from the docs and paste it into your script.

Now, let's return to the Fast MCP documentation and see how to create a prompt using the `@prompt` decorator. Copy the example code and add it to your script. You'll notice that the prompt takes two input arguments—`language` and `task_description`, both strings—and returns a `PromptMessage` type as output.

At this point, we have the three main building blocks in place: a tool, a resource, and a prompt. Let's try running the server to see if everything works.

The last thing we need is a main function to launch the server. Copilot can even help autocomplete this for you, which is pretty handy.

To start the server, check the CLI section of the Fast MCP documentation. You have a few options: you can run the Python file directly, or, if you want to use the MCP Inspector, you can launch it with `fastmcp dev server.py`.

If you encounter an error about missing type definitions for `PromptMessage`, make sure to import it correctly. Try importing `PromptMessage` and `TextContent` from `fastmcp.prompts`. Once that's done, the server should start, it runs on port 6274.

With the Inspector UI, you can use the web interface as a mcp client to explore the tools, resources, and prompts you've just created. For example, you can test the simple add tool by entering numbers, and it should return the correct result. You can also generate prompts by providing the language and task description arguments, and verify that the prompt is working as expected. Finally, you can check the resources, which are formatted and ready for use by the LLM.

Now that we've built a simple example with all three components. let's take a moment to dive deeper into what makes each of these building blocks unique.

Anthropic has got a helpful slide that explains the key differences between tools, resources, and prompts. Understanding these distinctions is important, even though it might seem a bit confusing at the first time.

- **Tools** are model-controlled. This means the AI model decides when and how to use them during its reasoning process. So, it's invoked by the LLM.
- **Resources** are application-controlled. These are pieces of data or configuration exposed to your application.
- **Prompts** are user-controlled. They allow users to provide specific instructions or context that guide the model's behavior.

Not all MCP clients currently support all three building blocks. As of today, most IDEs (vs code copilot, Cursor, Windsurf) only support tools. If you want to see tools, prompts, and resources all working together, the best way is to use Claude Desktop.

Now, I will show you how to set this up on Claude Desktop.

Setting this up on Claude Desktop is straightforward. First, open the app and go to the Settings menu. Navigate to the Developer section and click on "Edit config." All configuration is stored in a file called the Claude Desktop configuration. Open this JSON file with any text editor.

Next, simply add the MCP server you just built to the configuration. You can specify how to launch your server—just as we did before, using the `uv` command or the MCP CLI.

Once configured, you'll see that under the Tools section, the "add" tool is now available for the LLM to invoke. For example, let's try a simple addition: enter 3 plus 90. The app will ask for your permission before invoking the tool—just click "Allow." The AI will then use the tool to calculate and return the answer.

Now, let's check out the other two components. Both prompts and resources appear under the Attachments section. If you click on the data config, you can view the configuration data attached to your chat session.

For prompts, clicking on a prompt will open a window asking you to input the required arguments, just as we specified earlier. For instance, you can enter "Python" as the language and ask it to write a scraper for Booking.com. Add a simple instruction, such as "Just output the code." The application will attach this prompt to the request sent to the LLM.

After a few seconds, you'll see that the Python script for the Booking.com scraper has been generated. The output will include key features, usage instructions, and important notes, all created by the AI using the prompt and resource attachments.
