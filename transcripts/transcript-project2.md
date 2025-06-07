Hey everyone, welcome back! This is Project Two of the MCP From Zero to Hero series.

If you haven’t watched Project One yet, please check it out first. Project One covers the basics of MCP and shows you how to build a simple Confluence MCP server using FastMCP.

In Project Two, we’ll take things further and focus on making your MCP server production-ready. This project is a comprehensive guide to building an enterprise-grade MCP server with advanced features, including:

- Unit testing
- Multiple transport protocols
- Authentication mechanisms
- Remote server deployment

Project Two builds on the Confluence MCP server from Project One, adding features that are essential for real-world, production deployments.

Here’s what you’ll learn by completing this project:

- How to implement thorough unit testing for your MCP server using pytest
- How to understand and configure different transport protocols for MCP communication
- How to add authentication for secure API access
- How to deploy your MCP server to remote environments with proper configuration
- Best practices for developing and deploying production-ready MCP servers

Let’s talk a bit more about testing. In this project, you’ll learn how to:

- Achieve complete test coverage for all MCP tools and client operations
- Properly mock external API calls for isolated testing
- Use reusable test fixtures for consistent test environments
- Automate coverage tracking and reporting
- Add a coverage badge to your README

By the end of Project Two, you’ll have a robust, secure, and fully tested MCP server that’s ready for production use.

As you can see in the README, the current test coverage of the repository is only 38%, which is quite low. Let's understand why the coverage is so low and how we can improve it.

First, I'll run the test suite using uv run pytest to see the current state. The output shows that some tests are failing, particularly in the client tests. Additionally, several files—such as config.py, utility functions, and server.py—have zero percent coverage. For example, we haven't created any test files for server.py, which contributes to the low overall coverage.

To address this, we'll take two steps:

Firstly, Increase the test coverage by adding tests for untested files and functions.
Secondly, Fix any failed test cases to ensure the test suite passes.
Let's start by writing tests for the files with zero coverage, and then move on to resolving the failed tests.

To understand the failed test cases, let's have our Copilot agent analyze the situation. First, we need to run `pytest` and review the output to identify which tests are failing and why the coverage is low. The agent will start by running the test suite and collecting the failed test cases along with their error messages. It will also review the relevant test files, such as `test_client.py` and `conftest.py`, which contains the test configurations. Next, it will check the current coverage report.

The agent provides an analysis of the main causes for the failed test cases, it contains:

1. Mocking issues and assertion mismatches.
2. Broken fixture setup for FastMCP contexts.
3. Missing test files.
4. Specific problems in the client tests, such as incorrect module imports for `atlassian confluence` APIs, and using keyword arguments instead of positional arguments in assertions.
5. Issues with the context manager in the app lifespan function.

Each of these issues should be addressed separately. It's important to instruct the agent to fix these problems one by one and commit each fix individually. This approach ensures that each change is tracked and reviewed properly. In the past, we've seen that if not instructed, the agent might batch all fixes into a single commit, which is not ideal.

For example, the first issue was a module name mismatch in the client test code. Instead of importing from `alissa.confluence`, it should import `confluence.client.ConfluenceClient`, as defined in our `client.py` source file. This was a simple oversight, but the agent was able to identify and correct it.

Another issue involved using positional arguments instead of keyword arguments in pytest assertions, such as with the `get_page` and `update_page` functions. This is a convention that was missed during the initial code generation, highlighting the importance of reviewing AI-generated code. While the AI saves significant time by generating boilerplate and test cases, human review is still essential to catch these subtle mistakes.

After making these corrections, the agent was able to generate a comprehensive commit message following the Conventional Commits standard, as specified in our README file.

There was a pre-commit hook failure due to formatting issues, simply the agent just ran the ruff formatter to resolve them before committing.

With these steps, the code for the first set of fixes is committed. Now, we can proceed to address the next issue.

For the second fix, we focused on resolving issues in the `test_tools.py` file. Here’s a summary of the changes made:

### Fix 2: Resolving Mock Context Issues in `test_tools.py`

#### Problem 1: Fixture Code for Mock Context

The tests expected `MockContext.RequestedContext.LifespanContext.Confluence`, but the fixture only provided `MockContext.LifespanContext.Confluence`. To address this:

1. Updated the fixture code to create a proper `MockContext`.
2. Created a request inside the `MockContext`.
3. Created a lifespan context at the `Conference` level.

This ensures the sequence is correct and matches the test expectations.

#### Problem 2: Module Name Mismatch

The test initialization incorrectly referred to `Atlassian.Confluence`. It was updated to use `Confluence.Client.Confluence`, as defined in the `client.py` source file.

#### Problem 3: Async Context Manager Misunderstanding

The agent misunderstood how the async function for the context manager was defined in `server.py`. Specifically, the `app_lifespan` function was confirmed to be an async iterator of app contexts.

To fix this:

- Updated the mock context fixture to return a context instance instead of an async generator.
- Simplified the static methods inside the `Tools` class to call the updated `MockContext` during test.
- Ensured the `MockContext` contains a `Conference API Client`.

#### Results

After applying these fixes:

- The tests in `test_tools.py` passed successfully.
- The changes were committed separately to maintain clear tracking of fixes.

### Test Coverage Update

With these fixes, the test coverage increased from **38%** to **48%**. This is a significant improvement, but there’s still more to do.

### Fix 3: Adding Tests for the Config Module

The config module is relatively straightforward, as it primarily consists of a `Config` class that loads environment variables. To improve coverage, we added tests to ensure the following:

These tests were simple to implement and resulted in full coverage for the config module. The changes were committed separately to maintain clarity.

---

### Fix 4: Adding Tests for Utility Functions

The utility functions, created in Project One, were tested next. These functions are basic helpers, such as string manipulation, data validation, and API response formatting. The following tests were added:

These tests were straightforward, and the Copilot agent handled them effectively. For detailed implementation, refer to my GitHub repository, which contains all the source code and test files.

---

### Addressing Coverage in `test_client.py`

There was a question about whether `test_client.py` should aim for 100% coverage. Currently, it stands at 89%, primarily due to untested exception handling scenarios. As the Copilot agent suggested, testing exception scenarios depends on their importance. Here's the approach:

1. **Critical Exceptions**: Tests were added for null response handling, network-related errors, and CQL query failures.
2. **Non-Critical Exceptions**: Logging errors and simple re-raise scenarios were skipped, as they don't significantly impact functionality.

This decision balances thorough testing with practical development priorities.

---

### Updated Test Coverage

After completing these fixes, the test coverage increased from **48%** to **72%**. This is a substantial improvement, and the MCP server is now much closer to being production-ready.

---

### PyTest Tutorial: A Quick Guide for Beginners

Before we dive into the other sections of this course, I think we should create a quick tutorial on PyTest. If you're already very familiar with PyTest and don't feel you need to go through this session, feel free to skip it. For those of you who are new to PyTest or want a refresher on how it works, please bear with me for 5 to 10 minutes as I walk you through the basics of PyTest and explain how it's being used in this project.

First of all, what is PyTest? PyTest is Python's most popular testing framework. It makes writing and running tests simple while providing powerful features for complex testing scenarios. It's essentially a testing framework where you can simply run the command `uv run pytest` to generate a test report that shows you whether your test cases pass or fail, as well as the test coverage of your current project.

Let me explain a few key concepts:

#### 1. Basic Test Structure

The most fundamental concept is the basic test structure. Tests are functions that start with the prefix `test_` and use assert statements to check whether values are correct. This is the "Hello World" of basic test examples.

For example, we have a `test_basic_example` function with the `test_` prefix. The result is `2 + 2`, which equals 4. The assert statement will check and assess whether the test fails or passes. If the result equals 4 and does not equal 5, then the test passes.

#### 2. Fixtures: Reusable Test Data

The second concept is called fixtures. Think of fixtures as reusable components within the PyTest framework. Fixtures provide consistent test data and setup. They are decorated with `@pytest.fixture` and can be reused across multiple tests as many times as you like.

In our real-world example, we have many fixtures under a file called `conftest.py`. What it does is provide reusable components for certain objects. For example, the `mock_config` fixture provides a config object that can be used across the whole project. All it contains is a Confluence API config with the company's Confluence URL, username, and API token. These are all dummy configs used across the whole test suite, but they need to be called multiple times. Hence, we use the `@pytest.fixture` decorator to make our job easier.

You can see a second example with `mock_page`. This mock page returns a dummy page with page parameters like ID, title, space key, version, and content. This is a dummy page that might get called multiple times, which is why we create a fixture to make our testing more convenient.

Here's an example: if we need to test config values, you can always call `mock_config`, which returns a config object with all the parameters in it.

#### 3. Patching: Mocking External Dependencies

The third concept is called patching. Patch works like an interceptor when you make an API call or call a certain function. How it works is you put a `@patch` decorator, and when the Confluence client is called, it's actually not going to trigger the real Confluence client. What it triggers is a patched, fake Confluence client that provides dummy data during the test.

All it does is help you verify that your client initialization code can trigger a Confluence client initialization correctly. We don't actually worry about whether the real API call is made or not - we just need to verify that the initialization of the Confluence client is correct. Hence, we use the patch to provide a fake one during testing.

There's another example where you can mock an environment variable using `@patch.dict`. You can put your Confluence URL in it, and when we load the config, it will load the fake Confluence URL during testing.

#### 4. Async Testing

The fourth concept is async testing. If we need to test async functions, we need to use the decorator `@pytest.mark.asyncio`. We use this in `test_tools.py` when we need to call a function that is asynchronous, like `get_page_tool`. We have a page ID, and we need to set up a mock response. This is the way we test async functions.

For any asynchronous functions, we need to use `@pytest.mark.asyncio` to identify it as an asynchronous test function - essentially, it's a test function for asynchronous processes.

#### 5. Exception Testing

The fifth concept is exception testing - testing that your code properly handles errors using `pytest.raises`. You can see we're putting a wrong page ID on purpose. When the exception is raised, we use `pytest.raises` to check whether the exception is raised properly.

#### 6. Parametrized Testing

The last concept is parametrized testing. This allows you to run the same test with different inputs using `@pytest.mark.parametrize`. What it does is help you test the same function with six different inputs to see if they all can pass the test. So one function with six different inputs - that's why it's called parametrized testing.

#### Common Testing Patterns in Our Project

At a higher level, these are the testing patterns we use in our project:

1. **Setup-Action-Assert Pattern**: Very easy to understand. We set up mock data, then we take an action (which is normally a function call or API call to check the process), then we assert the result to check whether it's correct or not.

2. **Mock Configuration Pattern**: We use the `@patch` decorator to mock an API response, then we assert the response is what we expected.

3. **Context Manager Testing**: Remember in this project, as part of FastMCP, we use a context manager to manage the Confluence API client. During testing, we need to mock the context manager so all the Confluence client initialization can be mocked and handled during testing.

#### How to Run Tests

These are the test commands you'll need for PyTest. Most of them you've already seen in my videos. If you want to generate a coverage report on certain classes or in different report formats, you can always use those extra command parameters and arguments.

#### Test Structure Organization

You'll see this from my folder structure:

- **`conftest.py`**: At the very top, this contains shared fixtures and test configuration
- **`test_client.py`**: For testing the Confluence API client
- **`test_tools.py`**: For testing the MCP tools class, which has static methods under it
- **`test_config.py`**: For testing the config file used for loading environment variables and other constants
- **`test_server.py`**: For testing the main server initialization using FastMCP
- **`test_utils.py`**: For testing utility functions

That's it! Now we have a pretty good understanding of PyTest. If you have any further questions, you can always leave them in the comments under this video, and I'll be more than happy to answer them.

---

Now, I’m not going to show you the full details of the remaining test code generation, as it very much follows the same pattern. It continues with `test_tools.py`, along with updates to `update_coverage_page.py`.

What we achieved at the end is **98% test coverage**, which is phenomenal and ensures that our MCP server is robust and production-ready.

If you have any further questions, feel free to leave them in the comments section below, and I’ll be happy to help address them.

### Adding PyTest to Pre-Commit Hook

Now that we’ve achieved 98% test coverage, there’s one final step to ensure our testing process is seamless: integrating PyTest into the pre-commit hook. Previously, PyTest wasn’t included in the pre-commit configuration because the coverage was too low and several test cases were failing. Now that we’ve resolved those issues, it’s time to update the pre-commit hook.

#### Steps to Update the Pre-Commit Hook

1. **Modify `.pre-commit-config.yaml`**:
   Add a new entry for PyTest in the pre-commit configuration file. This ensures that the test suite runs automatically before every commit.

   ```yaml
   -   id: pytest
        name: Run PyTest
        entry: pytest
        language: python
        types: [python]
   ```

   - id: pytest
     name: Run PyTest with Coverage Threshold
     entry: pytest --cov --cov-fail-under=90
     language: python
     types: [python]

2. **Reinstall Pre-Commit Hooks**:
   After updating the configuration file, reinstall the pre-commit hooks to apply the changes. Run the following command:

   ```bash
   pre-commit install
   ```

   This ensures the updated hooks are active in your local codebase.

3. **Update `pyproject.toml`**:
   Make a small update to the `pyproject.toml` file to ensure compatibility with the pre-commit hook. For example, you might need to specify the test dependencies explicitly under `[tool.poetry.dependencies]` or `[tool.poetry.dev-dependencies]`.

   ```toml
   [tool.poetry.dev-dependencies]
   pytest = "^7.0"
   pytest-cov = "^4.0"
   ```

4. **Commit the Changes**:
   Once the pre-commit hook and `pyproject.toml` file are updated, commit these changes to your branch. Use a clear commit message following the Conventional Commits standard:

   ```bash
   git add .pre-commit-config.yaml pyproject.toml
   git commit -m "chore: add PyTest to pre-commit hook and update dependencies"
   ```

#### Results

With these updates, every commit will automatically run the test suite, ensuring that no code is committed without passing tests. This is a crucial step for maintaining code quality and preventing regressions in a production-ready MCP server.

Now that we've completed the unit tests and achieved 98% test coverage, the next step is to explore different communication transport protocols in more detail. Let’s dive into this topic by experimenting with our `server.py` script.

### Exploring Communication Transport Protocols

#### Standard IO Protocol

Let’s have a deep dive of the three different communicaition transport protocols. we can start with testing the Standard IO protocol. To do this, you can use the MCP Inspector tool without installing it by running:

```bash
npx @modelcontextprotocol/inspector
```

Once the inspector is up, it triggers the `server.py` script, spinning up the server in an isolated environment. For example, if you try the search function, it works as expected and returns the search payload for your PRD document.

#### Streamable HTTP Protocol

Next, let’s test the Streamable HTTP protocol. Unlike Standard IO, the MCP Inspector doesn’t directly trigger the server for this protocol. You’ll need to spin up the server manually. Run the following command:

```bash
fastmcp run server.py
```

For some reason, it did not work. The inspector will show you an error saying it can not find the server. Let's have a look at the FastMCP documentation, we learned that the default host and port are `localhost:8000` with the path `/mcp`. And with Fastmcp command, let's add `fasctmcp run server.py --transport -streamable-http` explicitly

```
INFO: Started server process [PID]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The search function then worked, returning the expected payload. A key takeaway here is that when using the `fastmcp` command without specifying the transport type, it defaults to Standard IO and skips the transport configuration in the main function. To avoid this, always specify the transport type in the command line arguments for non-Standard IO protocols.

Alternatively, you can bypass this by running the script directly with `uv`:

```bash
uv run server.py
```

This triggers the main function, where the transport protocol is already defined, eliminating the need for command-line arguments.

#### Server-Sent Events (SSE) Protocol

Finally, let’s test the Server-Sent Events (SSE) protocol. According to the FastMCP documentation, the default host and port are `localhost:8000`, and the SSE path is `/sse`. Although SSE is marked for deprecation in future versions, it still works in the current version.

To test SSE, you can either specify the transport type in the main function and run:

```bash
uv run server.py
```

Or use the FastMCP command with the transport argument:

```bash
fastmcp run server.py --transport sse
```

In the MCP Inspector, select SSE from the dropdown, update the URL to `/sse`, and reconnect. The search tool works as expected, returning the payload for the PRD document.

---

### Implementing Authentication in FastMCP

Now that we've learned about the three different transport protocols, it's time to look into authentication. Let's go through the FastMCP documentation and see how to set this up. I'll come back to the theory after we have something up and running.

#### Upgrading FastMCP for Authentication Support

First of all, we need to check if we have the latest version of FastMCP. Authentication has been included since version 2.6.0, so let's check our current FastMCP version to see if we need to upgrade it.

```bash
fastmcp version
```

As you can see, we only have version 2.3.3, so we actually need to upgrade FastMCP to include the latest authentication code. How do we do this? We simply need to run:

```bash
uv add fastmcp==2.6.0
```

This will upgrade FastMCP from 2.3.3 to 2.6.0, and then we can start using the new authentication classes.

#### Setting Up Bearer Token Authentication

Let's have a look at how we can set this up. The FastMCP documentation provides a clear guide on setting this up. First, we need to add the bearer auth provider for bearer token authentication. If you're not familiar with bearer tokens or how the authentication workflow works, don't worry too much about it - I'll come back to the theory once we have something set up.

Let's copy the example code into our codebase in `server.py`:

```python
from fastmcp.server import server
from fastmcp.server.auth import BearerAuthProvider
```

When we start the server instance, we need to add a few more components. We need to start the auth provider before we get the FastMCP server instance:

```python
auth_provider = BearerAuthProvider()
```

Now we need to check what we want to include here. To test this in our local environment, we can use a helper utility class called RSAKeyPair. What this does is generate testing tokens for us in the local environment without the need for using an OAuth2 provider externally.

Let's add this to do a quick test:

```python
from fastmcp.server.auth.bearer import RSAKeyPair
```

We'll generate the key pair before we can use it, so put it before the bearer auth provider:

```python
key_pair = RSAKeyPair.generate()
auth_provider = BearerAuthProvider(public_key=key_pair.public_key)
```

And of course, we need to add the auth argument to the FastMCP instance so the server will have authentication enabled. Unauthorized or unauthenticated users or clients will not be able to talk to the server:

```python
app = FastMCP("Confluence MCP Server", auth=auth_provider)
```

For testing purposes, we can even print out the token to check and validate whether it's been generated:

```python
print(f"Test token: {key_pair.create_token()}")
```

Let's quickly spin up the server in our local environment to see if it works. If we run `uv run server.py`, cool! As you can see, the test token is already being generated and saved, and it's used by the server.

#### Testing Authentication with FastMCP Client

So how do we validate if the authentication is working? One simple way to validate is to use the client class from FastMCP. FastMCP can not only be an MCP server, it can also be used as an MCP client. For testing purposes, this client instance we're spinning up is going to be super simple - it's just to test whether the authentication is working for us or not.

Reading through the FastMCP documentation on the client, pay special attention to the authentication part to see how it's going to be configured. The authentication of the MCP client is based on OAuth specifications. The most common use case is actually for machine-to-machine service communication. For example, we have a service account (which I'll show you later when we set up cloud hosting) that we'll use to invoke communication with the remote server.

The client will have an authentication header, and in that authentication header, we'll put the bearer token. That's normally generated by an OAuth provider, but for testing purposes, that token is generated by the RSAKeyPair utility class that we used in the server.

So we create a simple `fastmcp_client.py` file. What it does is initialize a client with the authentication token saved in the header, and it just makes a simple MCP call to the server, which is the `list_tools` command. If we can establish the connection, it will get a list of all the available tools and print them all out.

Let's test this example:

Cool, this is working. We have got all the tools listed in the response payload.

Now let's prove that authentication is actually working. Let's try to run the client again, but this time without putting the authentication token in the header.

As you can see, this time we get an error: **401 Unauthorized**. This proves that we do need authentication - the bearer token must be added to the header for the client to successfully communicate with the server.

---

### Deploying to Remote Cloud Host

Now that we have authentication working, we're approaching the final step of this project: deploying our MCP server to a remote cloud host. Let's compile a `server.py` that's ready for production use.

#### ASGI Server Integration for Production

For production use, we'll leverage FastMCP's ASGI server integration capabilities. Let's go to the FastMCP documentation - there's a section that talks about ASGI server integration. We can easily mount this MCP server on a Starlette ASGI server.

The good thing about mounting it to a Starlette server is that it becomes a proper backend server, which means you can have multiple routes and different endpoints on the backend API service. A very typical one is a health endpoint, which becomes very handy when you want to ping this health endpoint to check the status of the server and get a healthy status response.

To mount our MCP server, it's very simple. Just mount it inside the route and give it a path `/mcp-server`. The final path of our MCP server endpoint will be `/mcp-server/mcp`.

Apart from that, there's not much to change. We also need to pay special attention to the final main function - it's slightly different from our local server instance. Instead of using `mcp.run()`, we actually need to import Uvicorn and use `uvicorn.run()`. The host URL is no longer `localhost` - it's `0.0.0.0` for Cloud Run, and the log level should be set to `INFO`.

That's pretty much it - those are all the changes we need to make for a production-ready `server.py`.

#### Creating the Dockerfile

The next step is containerizing our server and deploying it to Cloud Run. For containerization, we need to create a Dockerfile.

Let me quickly go through what's in the Dockerfile I created for deployment:

```dockerfile
# Get the Python base image 3.11 slim
FROM python:3.11-slim

# Set environment variables for deployment
ENV UV_CACHE_DIR=/tmp/uv-cache

# Install UV from the public image
RUN pip install uv

# Create a non-root user following security best practices
RUN useradd --create-home --shell /bin/bash app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Switch to app user and sync dependencies
USER app
RUN uv sync --no-dev

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Final command
CMD ["uv", "run", "server.py"]
```

We also have a `.dockerignore` file to exclude non-production related files. You can see there's a big list of files that won't be copied into the Docker container, including the client test files we created for local testing purposes - they don't need to go to the production environment.

#### Deployment Script and GCP Setup

Now that we have Docker and dockerignore set up, the next step is to deploy to the cloud platform. In this instance, we'll use GCP. I'll also introduce you to AWS solutions later, but GCP offers the simplest solution for deploying remote servers with authentication at this stage.

For deployment, we have a simple shell script. First, it checks for a `.env` file with environment variables. We need three environment variables: Confluence URL, Confluence username, and Confluence personal access token. These get added during the deployment process as environment variables for our Cloud Run instance, so they're not exposed in the codebase - this follows security best practices.

We also set up several variables during deployment: Project ID, region, repository name, image name, and version tag.

Let me explain the whole process:

1. We have a Dockerfile in our local environment
2. First step: build a Docker image from the Dockerfile
3. Once built, it gets pushed to GCP's Artifact Registry
4. Artifact Registry is a collection of your private Docker images

If you go to Artifact Registry, you can see there's already a repository created called "fastmcp-repo". You can create as many repositories as you like, and our Docker image will be saved under this repository.

Pay special attention to the Docker build command. If you're running this on your ARM64 Silicon MacBook, we need to add the `--platform linux/amd64` argument, otherwise there will be compatibility issues. That's the instance type that Cloud Run uses - not ARM64 Apple Silicon processors.

Once the image is built and pushed to Artifact Registry, the final step is deploying a Cloud Run instance based on the uploaded image. That's where you set the environment variables for Confluence URL, username, and personal access token, along with other parameters.

Pay attention to this argument `--no-allow-unauthenticated` - this means API calls or MCP calls must be authenticated with cloud run.

#### Running the Deployment

Let's run the deployment script. First, authenticate with `gcloud auth login`, which will ask for access permissions.

run the `deploy.sh` script:

1. It starts building the Docker image (takes a few minutes)
2. Pushes the image to Artifact Registry
3. Deploys to Cloud Run

The deployment is successful when it says "serving 100 percent of traffic" and provides the service URL.

#### Testing the Remote Server

Now we need to update our client configuration to connect to the remote server instead of the local one.

#### Authentication Methods

To establish the connection, we need to firstly understand how the authentication with remote server works.
Google has documentation on how to deploy an MCP server to Cloud Run with streamable HTTP connection support. For authenticating MCP clients, there are two options:

1. **IAM Invoker Permission**: Uses a local Cloud Run proxy on your machine to securely expose the remote MCP server using your credentials. As long as your user credential has the `roles/run.invoker` permission, this works.

2. **OIDC ID Token**: Uses Google OAuth library to get OIDC tokens for authentication based on a service account.

If this is your first time using GCP, you'll need to install the Google Cloud CLI. Just search "install gcloud CLI" for instructions for macOS and Windows.

**Option 1: IAM Invoke Permission**

For the client, we need to spin up a local Cloud Run proxy using the command from Google's documentation:

```bash
gcloud run services proxy confluence-fastmcp --region=us-central1 --port=3000
```

The local proxy injects our user credentials and uses them to authenticate with the remote MCP server.

One important thing to remember: since we're using a Starlette server, it becomes a proper API backend server, so the endpoint is no longer `/mcp` - it's `/mcp-server/mcp`. We need to update this in our client script.

Once updated, let's run our client with the local proxy:

```bash
uv run client-with-local-proxy.py
```

Boom! It's working! We've successfully proved the first authentication method works.

**Option 2: OIDC ID Token**

Different from option one, which uses your user login credentials, option 2 uses an OIDC ID token. We need to use a service account here, so we'll be using the service account credentials to retrieve an ID token. OIDC stands for OpenID Connect ID Token.

For this approach to work, you'll need to provision a service account on GCP. Go to your GCP console and click on "Service Accounts", then create a new service account. You can name it "confluence-mcp-server" and click "Create and Continue".

Remember to add the permissions for invoking the Cloud Run server, which is the `roles/run.invoker` role. Once that's ready, just click "Continue" and you'll be able to provision the service account.

#### Setting Up Service Account Credentials

Once you have the service account ready:

1. Click on "Manage Keys" from the settings
2. Click "Create New Key"
3. The new key will automatically start downloading

Once you have the service account key ready in your downloads folder, grab it and save it in your `.config/gcloud` directory.

Next, go back to your codebase and add an environment variable called `GOOGLE_APPLICATION_CREDENTIALS`. This will contain the file path URL of that service account key you just saved.

#### Implementing OIDC Token Authentication

Once that's done, let's look at the script. First, we load the environment variable because we need to know the `GOOGLE_APPLICATION_CREDENTIALS` location.

We also have a token manager created to manage the OIDC ID token. The target audience in this instance is the URL of that Cloud Run instance. The token will initially be set to `None` and expires at 0.

The refresh is based on the condition: if we don't have a token (token equals `None`) or it's about to expire in the next 5 minutes, we refresh the token. We need to grab `GOOGLE_APPLICATION_CREDENTIALS`, which is the service account key that's saved in our local folder.

We use the `IdTokenCredentials` class to retrieve the ID token using our service account credentials. Once the token is retrieved, we refresh it and decode it to check the expiry date.

#### Main Function Implementation

When we get to the main function:

1. First, we grab the Cloud Run URL and the token manager
2. We set the transport to streamable HTTP with the Cloud Run URL: `/mcp-server/mcp/`

We need to pay special attention to the trailing slash here. Initially, I didn't add the trailing slash and started getting 307 redirect errors. I'm not 100% sure whether this is a Cloud Run thing or just a general requirement, but you need to add the trailing slash at the end of `/mcp` to make the whole thing work.

The rest of the code is straightforward - we're still just checking and listing the tools.

Let's run it and see if it returns a list of tools for us:

```bash
uv run client-with-oidc-token.py
```

Excellent! It's working perfectly. We've successfully demonstrated both authentication methods for connecting to our remote MCP server deployed on Cloud Run.

---

### Project Summary

Congratulations! We've successfully completed Project Two of the MCP From Zero to Hero series. Let's recap what we've accomplished:

#### Key Achievements

1. **Comprehensive Testing**: We increased test coverage from 38% to 98% by:

   - Fixing failed test cases systematically
   - Adding tests for untested modules (config, utils, server)
   - Implementing proper mocking strategies
   - Adding PyTest to pre-commit hooks

2. **Transport Protocol Mastery**: We explored and tested all three MCP transport protocols:

   - Standard IO (via MCP Inspector)
   - Streamable HTTP (production-ready)
   - Server-Sent Events (SSE, deprecated but functional)

3. **Authentication Implementation**: We implemented secure authentication using:

   - Bearer token authentication with RSAKeyPair for local testing
   - Two production authentication methods:
     - IAM Invoker Permission with Cloud Run proxy
     - OIDC ID Token with service account credentials

4. **Production Deployment**: We successfully deployed our MCP server to Google Cloud Run:
   - Created production-ready Dockerfile with security best practices
   - Implemented ASGI server integration with Starlette
   - Configured Cloud Run with authentication requirements

#### What You've Learned

Your MCP server is now robust, secure, fully tested, and ready for production use. This foundation will serve you well as you build more complex MCP integrations and scale your implementations.

In the next video, we will look into some more advanced topics and discuss the AWS solution on remote server hosting. Happy coding!
