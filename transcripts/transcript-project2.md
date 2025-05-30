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
