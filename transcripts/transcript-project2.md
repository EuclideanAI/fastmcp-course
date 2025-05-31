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

Now, let's examine the failed tests more closely. I'll use the verbose option with pytest to get more details about what's failing:

```bash
uv run pytest -v
```

Looking at the output, I can see that we have two main issues:

1. The `test_client_initialization` test is failing because we're passing parameters incorrectly
2. The `test_get_tool` function is failing due to mismatched response structures

Let's start by fixing the client initialization test. The issue appears to be that we're using positional arguments when the function expects keyword arguments. This is a common mistake that's easy to fix.

The error message shows that the `ConfluenceClient` constructor expects keyword arguments for `base_url` and `auth_token`, but our test is passing them positionally. Let's modify the test to use the correct parameter format.

I'm also noticing that several of our mocks are not set up properly. The test is expecting specific return values from mocked functions, but the actual implementation has changed since these tests were written.

Let's fix the mock setup in our `test_tools.py` file. The main issue is that the mocked response structure doesn't match what the code is expecting. We need to update our mock objects to return data in the format that the functions expect.

After fixing these initial test failures, we can focus on increasing our coverage by adding tests for untested files:

1. `config.py` - We'll need to test the configuration loading and validation functions
2. `server.py` - Tests for server initialization, request handling, and shutdown
3. Utility functions - Tests for helper functions in various modules

Let's first focus on the server.py file, as it's a critical component with zero coverage. We'll create a new test file called `test_server.py` and write tests for:

- Server initialization with different transport protocols
- Request handling and response generation
- Error handling
- Graceful shutdown

For testing the server, we'll use pytest fixtures to set up and tear down test environments, and we'll mock external dependencies to ensure our tests are isolated and repeatable.

With these changes, we should be able to increase our test coverage substantially. Our goal is to reach at least 80% coverage, which is a good benchmark for production code.
