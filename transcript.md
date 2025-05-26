Hey everyone, welcome to the MCP From Zero to Hero series. Before we get into the nitty gritty of the full course, I want to kick things off with a real-time demo so you can see MCP working in practice.

Alright, let's jump right in.

Imagine I'm a product manager and I type: "I need to create a PRD (Product Requirement Document) — for an AI-powered baby tracker app. The app should help parents track feeding times, sleep patterns, nappy changes, and growth milestones. It should use AI to provide insights and predictions about the baby's development. The target audience is first-time parents, and we want to emphasize ease of use and peace of mind."

As soon as I submit this request, you’ll notice the agent immediately detects the available tools from the Atlassian MCP server. It then starts generating a PRD in a `PRD.md` file. In just a few seconds, we have a comprehensive product requirement document for our baby tracker app.

But that’s not all. Let’s take it a step further. Suppose I ask the AI, "Can you refer to the software development template available in my company's confluence workspace?" The agent will connect to our Atlassian account, locate the relevant product requirement template, and use it as a reference.

Next, The agent triggers a tool from the Atlassian MCP server called Conference Search. It searches the Athletician Conference workspace for a few pages relevant to my query, along with their associated metadata. Then, it runs another tool called 'get page' to fetch the full content.

After a brief moment, the agent confirms: "I have successfully created a new Confluence page for your Baby Tracker app. Here’s what I’ve included." If we refresh our Confluence workspace, we’ll see a new page titled "Product Requirements – AI Powered Baby Tracker," complete with objectives, problem statements, target audience, user personas, and success metrics.

The document covers everything: comprehensive baby activity tracking, reducing anxiety for new parents, creating a positive user experience, driving growth and retention, and outlining a sustainable business model. It even lists assumptions, core features, and delivers detailed requirements.

What’s especially impressive is that the agent formats tables and sections to match the Confluence template—not just plain markdown. It converts the draft content to align perfectly with the company’s formatting standards.

---

Here’s what we’ll cover in today’s episode:

First, I’ll introduce what MCP—the Model Context Protocol—is, why it matters, and highlight its key features and benefits.

After that, we’ll set up your development environment together and create your very first MCP server. I’ll explain the core building blocks of MCP: Tools, Resources, Prompts, and Context.

This is a hands-on tutorial, so we’ll dive right into building a Confluence MCP server from scratch. Then, I’ll show you how to integrate it with VS Code Copilot and Claude Desktop.

We’ll also discuss the main communication transports, including SSE, and cover authentication for remote servers and important security considerations.

Moving into advanced topics, I’ll demonstrate how to mount MCP onto an existing FastAPI project.

Finally, I’ll show you how to deploy your MCP server—creating a Docker file and deploying to GCP or any other cloud platform.

And as a sneak peek, in the next course, I’ll teach you how to build an MCP client and your own user interface from scratch.

Without further ado, let’s get started with the introduction!

MCP stands for Model Context Protocol. It's a standardized way for AI models to communicate with various tools and services. Think of it like a universal USB-C connector for AI applications—one standard that works regardless of which AI model or tools you're using.

Just like USB-C lets you use the same cable to connect different devices, MCP makes your AI integrations portable. You can easily swap out one AI model or client for another without having to rewrite all your code.

This modularity means you spend less time on custom integrations and more time building features that matter.And because MCP is a standard, it means everyone integrates with large language models (LLMs) in the same way. Instead of writing custom, one-off code for each new model or tool.

Plus, MCP helps future-proof your projects. As new AI models and tools emerge, you can plug them into your existing setup with minimal changes—just like plugging a new device into a USB-C hub. This flexibility and simplicity are what make MCP so powerful.

Let’s take a moment to explain how MCP works, especially in the context of one of the biggest recent advancements in AI: function calling.

Function calling is a breakthrough that’s enabled large language models (LLMs) to use tools and APIs—much like how humans use tools to extend their abilities. In human history, one key difference between us and other primates is our ability to understand and use tools. The same principle now applies to LLMs.

Here’s the basic idea: In programming, you define functions or methods that perform specific tasks. With function calling, you can provide these function definitions to an LLM. When you send a query, the LLM decides whether it can answer directly or if it needs to use a tool (i.e., call a function). If a function call is needed, the LLM returns an action indicating which function to call and with what parameters. The actual function (or tool/API) is then invoked by your application, not by the LLM itself. The result is passed back to the LLM, which uses it to generate the final response for the user.

While function calling is powerful, it often requires custom code for every new tool, API, or authentication method, and can become complex as you scale.

This is where MCP comes in. MCP standardizes how tools are defined and accessed by LLMs. Instead of writing custom integration code for each new tool or API, you configure tools on an MCP server. Each MCP server can represent a service provider with a collection of APIs. The LLM simply decides when to use a tool; the MCP server handles the rest—tool invocation, authentication, and response formatting.

This approach means you don’t have to reinvent the wheel every time you build a new AI application. You just need an MCP client that can talk to an LLM or multiple LLMs (if needs to) and handle responses, while the heavy lifting is managed by the MCP server and service providers.

The portability and extensibility of MCP have been clearly demonstrated in just the last six months since its creation in November 2024. Thousands of MCP servers have already been created and shared across the internet. Several third-party MCP registries now host more than 10,000 MCP servers, covering a wide range of use cases—from data and file systems, development tools, web and browser automation, productivity, and communication.

There are also official integrations available. If you check Anthropic’s official GitHub repository, you’ll find a number of service providers that already offer official MCP servers.

OK, now it's time to get our hands dirty! There are no prerequisites for these sessions, and you don't need to be a Python expert to create an MCP server. There are just two things we need to know before we can start building.

The first is `uv`, a Python package manager. We'll use `uv` to install all our dependency packages. The second is FastMCP. You can visit its website to learn more about what FastMCP is. The name is inspired by a very popular python backend package called FastAPI — FastMCP provides a high-level interface library built on top of the original Python MCP SDK. The benefit is that it's fast to build with, simplifies the development process, reduces boilerplate code, and is very Pythonic and beginner-friendly.

To install UV is pretty straightforward. Just follow the instructions on the UV documentation—it works for both macOS and Windows users. There are two simple commands you need to run, depending on your operating system. Once UV is installed, you don’t need to manually download Python yourself. UV can automatically install and manage different Python versions for you. It’s a fully managed solution that provides an excellent way to handle Python versions and dependencies across multiple projects.

Let's get started:

1. First, use `uv init` to create a new project.
2. Then, run `uv add fastmcp` to install Fast MCP and all its dependencies. This only takes a few seconds.
3. If you're curious, you can check the `uv.lock` file to see all the dependency information.

After installation, you'll want to activate your virtual environment. Once you're inside the `.venv` environment, you can check the Fast MCP version by typing `fastmcp --version`. This will display the current Fast MCP version as well as your Python version.

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

## Starting Our First Project: Building a Confluence MCP Server

Now we're ready to start our first real project - building a Confluence MCP server! This project will guide you through the complete process of creating a functional MCP server.

I've created a repository called `fastmcp-course` You can find the link in the description below this video to clone the repository.

In this course series, there are 3 projects in total:

**Project 1** focuses on building and setting up a Confluence MCP server integrated with VS Code Copilot and Claude Desktop.

Today, I will guide you through Project 1 step-by-step.

After project 1 you will learn how to:

## What You'll Learn

- Build a complete MCP server for Confluence to:
  - Search, retrieve, create, update, and delete Confluence pages
  - Get page children and ancestors for hierarchical navigation
  - Manage comments and labels
  - List and navigate across Confluence spaces

## Development Setup

As I mentioned before, you'll need:

- Python 3.10 or higher
- UV, the Rust-based Python package manager

First, make sure when you clone the repository, you specifically checkout the `project-one` branch:

```bash
git clone -b porject 1 https://github.com/euclideanai/fastmcp-course.git
cd fastmcp-course
```

This branch will give you all the essential files to get started without including the final solution (which is available in the main branch). This approach gives you a clean starting point while still allowing you to build the project yourself.

You can just do `code .` from your terminal to open up the VS Code terminal, or you can just open VS Code and choose the FastMCP course directory.

Once you're in there, there's one important thing that I need to mention to you: the system prompts. It sits under `.github/prompts.md`. This is an important system prompt directory that Copilot will read before every conversation.

So why is it important? Because what I have written here is a project guideline. In this project, we'll use GitHub Copilot agent to do all the groundwork for us. That includes setting up the classes, file directories, and all the boilerplate code. So this guideline is critically important—it pretty much provides the guidelines for the coding practices for the Copilot agent to follow.

The API we will use is called Atlassian Python API. It's an existing package that we can leverage for all the API calls we need to Confluence.

We also list out the folder structure so when the code generated by the agent, it will strictly follow what's being provided in the guideline, without derailing to some overly complicated solutions.

It also lists the environment variable names for the agent to follow.

We also listed out the error handling strategy and test strategy, so the agent knows how to write test codes based on this guideline.

We've included code examples from the FastMCP documentation, with special attention to the `AppContext` class. This class serves as a context manager for asynchronous processes, wrapping our Confluence client. This approach allows us to reuse the same client for multiple API calls without reinitializing it for every request.

There's also a code snippet demonstrating how to create a search tool class, providing an example for the agent to follow. Finally, we've specified how tools should be registered with the FastMCP server using the recommended `mcp.at_tool_class` function.

While this might seem like a lot to process at first, everything will become clearer once we start implementing the project.

## Let's Begin the Implementation

First, let's run `uv sync` to install all the dependency packages based on our `pyproject.toml` file. This will ensure we have all the required packages before we start coding.

Now, let's go to the Copilot agent chat window, select the agent mode, and pick Claude 3.7 Sonnet as our model. We'll type our first prompt based on the project architecture we specified in the planning prompt MD file:

"Based on the project architecture which we specified in the planning prompt MD file, please complete the implementation of our Confluence MCP server."

Now, once we hit submit, it will start generating the code for us. You can see it says it's starting to read those files that we pre-created for these tasks. It's reading `server.py` to understand the main functions, and it's reading the `pyproject.toml` to understand the dependencies and project requirements. It's reading through the README `planning.prompt.md`.

OK, it says it has got a good understanding of the project now and starts to make new directories. It's exciting! Just click on continue. You can see a few new directories have already been created by the agent.

You can see it's now generating the `config.py` file as well as the `client.py` in the models directory under the confluence directory.

It's creating the basic structure for our project, following the guidelines we specified. The agent is setting up all the necessary components for our Confluence MCP server.

In the `config.py` file, it's defining configuration settings that will allow our server to connect to the Confluence API. This includes setting up environment variables for authentication credentials and base URLs.

Meanwhile, in the `client.py` file under the models directory, it's implementing the core client functionality that will handle the actual communication with Confluence's servers. This is where all the API interactions will be managed.

As the agent continues to work, it's also creating model definitions that will represent Confluence data structures in our application. These models will help us maintain type safety and provide clear interfaces for working with Confluence data.

This automated setup process is saving us a tremendous amount of time by handling all the boilerplate code and creating a well-structured project architecture. The agent is following best practices and implementing patterns that will make our code maintainable and extensible.

Let's watch as it continues to build out our project structure, creating the various tools and utility classes we'll need for our Confluence MCP server.

The code generation is now complete. Let's clean up a few issues with the implementation.

First, looking at the `server.py` file, I notice that `mcp.lifespan_handler = app_lifespan` is incorrect. This needs to be fixed since our implementation uses the proper context manager approach.

After reviewing the rest of the `server.py` file, everything else looks good. Let's examine the other files for potential issues.

In `client.py`, AI has implemented exponential backoff for better reliability on API calls. There's also an issue with the `response` variable potentially being `None`, which could cause errors.

Looking more closely at the `ConfluenceClient` class, I see that multiple methods have the same issue with response handling. Rather than fixing each one individually, I'll ask the agent to address this common error pattern: "The response could be None and this null value needs proper handling in each function."

The agent quickly identifies and fixes the response variable handling in all relevant functions, ensuring we don't have null reference errors.

There's also an issue with a `version` variable that's commented out but being referenced elsewhere in the code, which needs to be addressed.

Next, I examine the test files (`test_tools.py` and `test_client.py`) to ensure they're properly implemented. I ask the agent how unit tests are supposed to be run in this repository.

The agent analyzes the `pyproject.toml` file to understand the testing configuration and explains that we can simply run the tests using the `pytest` command.

However, I notice there's a reference to a `request_context` in the test files, but this doesn't exist in the FastMCP library. This is an error in the test code. Based on our server implementation, we're using an `AppContext` class for this purpose.

I also encounter an issue where pytest isn't installed in our environment, which is preventing us from running the tests properly.

After reviewing these issues, let's install pytest to run our tests properly:

```bash
uv add pytest --dev
```

Now that we have pytest installed, we can run the tests to verify our implementation:

```bash
python -m pytest
```

However, before running the tests, we need to fix the `request_context` reference issue in our test files. The correct implementation should use our `AppContext` class instead.

## Testing Our MCP Server

Now let's spin up our Fast MCP server by typing `fastmcp dev server.py`. It will trigger the MCP inspector. Just need to click on "Connect".

As you can see now, if you click on the "Tools" section, it will list out all the tools that we have built in our code repository.

Looks like we have encountered an error. So let's go back to our code and see what this error is.

## Debugging and Fixing Our MCP Server

Now that we've discovered an error, let's go back to our code and fix it.

When we examine the `server.py` file, we notice that there's a fundamental issue with the initialization order. The MCP instance gets created before the `AppContext` definition, which means the Confluence client never gets properly initialized and picked up by the server.

```python
# Current problematic order
mcp = FastMCP(name="Confluence MCP Server", description="Access and manage Confluence pages and spaces")

# AppContext defined after MCP initialization
class AppContext:
  # context manager code...
```

To fix this, we need to:

1. Move the FastMCP instance initialization to be below the AppContext class definition
2. Add the app_lifespan parameter to properly connect our context

After making these changes, we can use `ruff` to format our code:

```bash
uv run ruff format server.py
```

Now let's start the server again and see if our changes resolved the issue:

```bash
fastmcp dev server.py
```

After reconnecting to the server, let's test our tools. If we go to the "Tools" section, we can now see a list of all available tools. Let's try the "get_page" tool by providing a page ID.

For now, let's untoggle the "body" option. When we run the request, we can see it has been processed successfully! Now if we toggle the "body" option on, we should be able to see the complete page content. There it is - the content in HTML format has been successfully fetched by our MCP "get_page" tool.

## Testing Page Creation

Now, let's test creating a new page using our MCP server.

Let's try the "create_page" tool with these parameters:

- Title: "New Page Test"
- Content: "This is a new page"
- Space key: "SD" (abbreviation for Software Development)

When we hit "Run", we can see that a new page has been successfully created! Let's refresh our Confluence instance to confirm - and there it is! "New Page Test" has been created by our MCP tool.

## Testing Child Page Creation

Next, let's try another operation - creating a child page under an existing parent page.

For this, we need to use the "create_page" tool again, but this time we'll provide a parent ID. Let's use the ID "643-3529".

Hmm, we're getting an error: "The input should be a string type". Looking at our tool implementation, it appears the tool is validating that the parent ID field should be a string, but we might be passing it as a number.

Let's check the definition of the "get_page" tool:

```python
@mcp.tool
async def get_page(
  page_id: str,
  expand: Optional[str] = None,
  status: Optional[str] = None,
  version: Optional[int] = None,
  body: bool = False
) -> Dict:
  """
  Get a Confluence page by ID.

  Args:
    page_id (str): The ID of the page to retrieve.
    expand (str, optional): Comma-separated list of properties to expand.
    status (str, optional): Filter by status (e.g., 'current', 'draft').
    version (int, optional): The version number to retrieve.
    body (bool, optional): Whether to include the page body in the response.

  Returns:
    Dict: The page data.
  """
```

Indeed, we can see that `page_id` is defined as an optional string field. We need to ensure we're passing the parent ID as a string rather than a number when using the tool.

To fix this, simply change the string to int in type validation under before `search_tools.py` and `client.py`.

There we go, after the fix, a child page now is created under the parent page.

## Testing Page Updates

Let's try another operation - updating an existing page. For this, we'll use the "update_page" tool and provide the page ID "6422529".

We'll change the title to "MCP from Zero to Hero" and set the content to "Project One" as a simple update. Let's also provide a version comment to track our changes.

When we click "Run," we can see that the update has been processed successfully! Let's refresh our Confluence space to verify the changes have taken effect.

Perfect! There it is - "MCP from Zero to Hero" - our title has been successfully updated.

## Testing Page Deletion

Finally, let's test the page deletion functionality. We'll use the "delete_page" tool and provide the ID of the child page we just created earlier.

After entering the page ID and clicking "Run," the operation completes successfully. Let's refresh our Confluence space to confirm the deletion.

As expected, the page has been removed from our Confluence space, confirming that our delete operation is working correctly.

## Fixing Return Messages

Now that the page tools are working, you may notice a small issue with the return message. Although the operation is successful, the return message still indicates an error. Let's go back and fix this in our code.

Instead of returning just the result, we will return a dictionary with two attributes: `status` and `page_id`. The `status` will indicate success, and the `page_id` will include the page ID. After making this change, we test the delete page operation again. Now, the correct message is returned once the operation is successful.

## Testing the "Get Page Children" Tool

Next, let's test the "get page children" tool. To do this, we create a child page under "MCP from Zero to Hero" and name it "Project One." We add a single sentence as example content and publish it.

After grabbing the page ID of "MCP from Zero to Hero," we run the tool. As expected, it successfully retrieves its child page, "Project One."

## Testing the "Get Page Ancestors" Tool

Now, let's test the "get page ancestors" tool. This time, we work in reverse. We grab the page ID of "Project One," input it into the tool, and run it. The tool successfully retrieves its parent page, "MCP from Zero to Hero."

That's all done for the page tools. Now we can move on to the search tool.

## Testing the Search Tool

Now, let's test the search tool. We'll start by searching for "PRD" in the Software Development space. Initially, the tool runs but returns an error stating that the query cannot be parsed. Let's investigate this issue.

Upon reviewing the code, we notice a problem. There's a variable called `CQL` being used inside an `if` statement, but it hasn't been declared outside of it. This causes the `CQL` variable to always be undefined, regardless of how the logic is handled.

To fix this, we declare `CQL` as an empty string outside the `if` statement. After making this change, we run the tool again. However, the error persists, and the query still cannot be parsed.

Next, we check the logs for more details. The issue becomes clear: when the `CQL` variable contains a simple word like "PRD," it doesn't get enriched into a proper CQL statement. Instead, it remains as plain text, which the Confluence API cannot process.

To resolve this, we modify the code to handle simple text queries. If the input is a single word, we prepend the `text` keyword to convert it into a valid CQL query. This ensures the query is properly formatted before being passed to the `confluence.cql` function.

After implementing this fix, we run the tool again. This time, the search executes successfully, and we can see the expected results for "PRD" in the Software Development space.

Yeah, there are a few more tools e.g. get_spaces, get_comments, add_comments, get_labels etc. that I'm not going to go through in detail right now. You can try them when you start working on your project.

Now, what I want to quickly show you is the final integration with Claude Desktop and GitHub Copilot.

As I showed you before, you can configure Claude Desktop by editing the desktop config file. Simply specify the directory where your MCP server is located. Make sure you provide the correct directory path in the config file and use `uv fastmcp` to run the server.

Once the server is running, you can see the tools are already available in the Claude Desktop UI under the "Tools" section. Let's quickly try a prompt. For example, ask the AI to fetch pages that talk about "Baby Tracker" from Confluence.

The AI will likely ask for your permission first. Then, it will trigger the "search_confluence" tool, which finds three pages relevant to the Baby Tracker app.

Now, let's do the same on GitHub Copilot. First, go to the `settings.json` file and ensure you've specified the correct directory. After that, type another prompt. This time, let's ask the AI to create a new page named "MCP Setup Guide."

The AI will first search for the available spaces in your Confluence account. It takes a logical approach—before creating a page, it checks how many spaces are available. It finds two spaces and determines that the "Software Development" space is the most appropriate for technical documentation.

Next, it starts creating the page. Perfect! Now, let's go back to our Confluence workspace, refresh it, and as you can see, there's already a new page created called "MCP Setup Guide."

## Recap

Cool, that's the end of the Project One. I hope you enjoyed it! Let's quickly recap what we’ve learned today.

First, we set up the project using the `planning.prompt.md` file located under the `.github/prompts` directory. This file provided a general guide for the AI to follow, including the folder structure, package management, code quality standards, and coding practices. It also included code examples from FastMCP to serve as guardrails for the AI during development.

We used GitHub Copilot in agent mode with the Claude 3.7 Sonnet model to generate the boilerplate code for the project. The project followed a well-organized folder structure:

- **`server.py`**: The main entry point for our MCP server.
- **`confluence/` directory**: Contains the Confluence client class, which includes the client implementation, data models for Confluence objects, and utility functions for parsing and handling API responses.
- **`tools/` directory**: Houses the tool classes. Each tool class is organized by functionality, such as page tools, and uses static methods to define individual tools. This approach, recommended by FastMCP, keeps the code clean and maintainable.

When registering tools, we used a simple `register_tools` function in the main entry point to register all tools from the different tool classes. This approach ensures the code remains simple and easy to follow.

We also paid special attention to the **context manager**. The `app_lifespan` function wraps the Confluence client in a context manager, ensuring we don’t need to reinitialize the client for every API call. Additionally, we ensured the FastMCP server was initialized correctly and that the lifespan function was properly attached.

Throughout the course, we saw how powerful AI tools LLM like Claude 3.7 can be in automating much of the development process. However, we also learned that AI can make mistakes, such as the issue we encountered with the CQL function. This highlights the importance of reviewing and validating the generated code to ensure correctness.

Finally, we demonstrated how to integrate the MCP server with Claude Desktop and GitHub Copilot, enabling you to use it seamlessly in your daily workflow.

With this foundation, you’re now equipped to build and extend your own MCP servers. Great job completing Project One, and I look forward to seeing you in the Project 2!
