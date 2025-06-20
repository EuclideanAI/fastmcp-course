**[On Screen: Animated MCP logo, upbeat music]**

Have you ever wondered why even the biggest AI companies sometimes get their specs wrong? Today, we’re diving into a real-world example from Anthropic—and what it means for you as an MCP engineer!

Hey everyone, welcome back! This is Project 3 of the MCP From Zero to Hero series.

If you’re new here, I highly recommend checking out Projects 1 and 2 first—they’ll give you the foundation you need for today’s deep dive.

**[On Screen: Quick flash of Project 1 & 2 thumbnails]**

## 1. The Anthropic Authentication Story

At the recent AI Engineer World’s Fair, Anthropic openly admitted they initially got the authentication spec wrong for remote MCP servers. Today, we’ll break down what went wrong, why it matters, and what’s changing in the new draft spec.

**[On Screen: Diagram of old vs. new authentication flow]**

## 2. Remote Server Deployment: AWS & GCP

Next, we’ll compare deployment options for remote MCP servers on AWS and GCP. I’ll walk you through reference architectures for both, highlighting best practices and common pitfalls.

**[On Screen: Split-screen AWS vs. GCP architecture diagrams]**

## 3. Deep Dive: Client-Server Communication

We’ll zoom in on how clients and servers actually talk to each other in MCP. Expect a hands-on look at the low-level engineering details, plus a quick demo on sampling and proxy servers.

**[On Screen: Code snippets, network diagrams]**

## 4. What’s New: The MCP Gateway

Finally, I’ll introduce you to the latest concept from Anthropic—the MCP Gateway, announced just a couple of weeks ago. We’ll discuss what it is, why it matters, and how it could change the way you build MCP integrations.

**[On Screen: “MCP Gateway” logo, feature highlights]**

That’s the roadmap for today! By the end of this episode, you’ll have a clear understanding of the latest MCP best practices, deployment strategies, and what’s coming next in the ecosystem.

If you find this helpful, don’t forget to subscribe and check out the GitHub repo linked below for all the code and resources. Got questions or want to share your own deployment tips? Please do drop them in the comments!

**[On Screen: Subscribe button, GitHub link, comment prompt]**

Let’s get started!

## Understanding the Remote MCP Server Controversy

**[On Screen: Diagram – Local vs. Remote MCP Architecture]**

To understand where the controversy around remote MCP servers comes from, let's rewind to the fundamentals of MCP.

Originally, MCP is designed for both local and remote hosting. In the local setup, both the MCP client and server run on the same machine, communicating via standard IO. This works on a trust model—no authentication or authorization is needed because both processes are under your control. That's why most open-source MCP repos today still default to local, standard IO setups.

But there's a downside: if you want to use multiple tools (like Confluence, Figma, Notion,github, etc.), you have to spin up a separate MCP server for each one on your local machine. Managing 10 different MCP servers locally quickly becomes cumbersome.

**[On Screen: List of local MCP servers for different tools]**

To offload compute and simplify your local environment, you might want to run MCP servers remotely. This is where things get tricky. Once the client and server are separated—say, your client runs on your laptop and the server is hosted in the cloud—you now have a classic client-server architecture. This means you need proper authentication and authorization at the transport layer.

Here's why this matters: when your MCP client connects to a remote server, it often needs to send sensitive credentials, like personal access tokens for services such as Confluence. If the remote MCP server is compromised or malicious, your credentials—and potentially confidential company data—could be at risk.

**[On Screen: Warning icon – Security risk of leaking tokens]**

Security is job zero. So, when you move MCP servers to remote environments, robust authentication and authorization become mandatory.

Now, let's look at how the original MCP spec (published March 26, 2025) approached this. The Anthropic team proposed that the remote MCP server should act as both an OAuth provider (authenticating clients and issuing bearer tokens) and a resource provider (serving tools, resources, and prompts). This dual role makes the MCP server much heavier—no longer just a lightweight "USB hub" for AI tools, but a full-fledged server with complex OAuth 2.1 responsibilities.

**[On Screen: Dual-role server diagram – OAuth provider + resource provider]**

Implementing OAuth is non-trivial. There are already specialized solutions for this, like Auth0, AWS Cognito, or Supabase Auth for Next.js stacks. Offloading authentication to these providers is often preferable to reinventing the wheel within every MCP server.

## The Updated Draft: Clean Separation of Authorization

**[On Screen: “New Draft Spec: Separation of Resource & Auth Providers”]**

Anthropic has updated the draft spec to incorporate this change. It introduces a clear separation between the MCP server (resource provider) and the external authorization server. For full details, you can check out the draft spec in the link below.

### Role Play: How the New Flow Works

Let’s walk through a 5-scene role play to illustrate the new flow. Our cast:

- **MCP Client:** “keyhope copilot”
- **Auth Provider:** (e.g., Auth0, Cognito)
- **MCP Server:** (e.g., Confluence MCP server)

#### **Scene 1: No Token, No Entry**

- **Client:** “Can I see this Confluence page? (No token)”
- **MCP Server:** “Nope! Show me your pass.”
   _(Returns HTTP 401 Unauthorized with a `WWW-Authenticate` header pointing to the auth guide.)_

#### **Scene 2: Discovering the Auth Provider**

- **Client:** “I’ve read the guide. Give me your metadata.”
   _(GET request to `/.well-known/oauth-protected-resource`)_
- **MCP Server:** “Here’s my metadata—including which authorization server to use.”

#### **Scene 3: OAuth 2.1 Flow (Standard)**

- **Client:** Initiates OAuth 2.1 flow with the Auth Provider.
- **Auth Provider:** Handles authentication and issues an access token (bearer token).

_(Standard OAuth 2.1 flow—see external diagrams for details.)_

#### **Scene 4: Access With Token**

- **Client:** “Can I see this Confluence page? Here’s my token.”
- **MCP Server:** “Token validated—access granted! Here’s your page info.”

**[On Screen: Sequence diagram showing client, auth provider, and MCP server interactions]**

## This new approach keeps your MCP server simple and secure, while leveraging proven authorization solutions.

## Remote Server Deployment: GCP

**[On Screen: GCP architecture diagram – highlight Cloud Run, IAM, OIDC, Artifact Registry]**

Let’s look at how to deploy a remote MCP server on Google Cloud Platform (GCP), following Google’s official guidance.

### Why GCP for MCP?

GCP offers a simple, cost-effective, and developer-friendly way to host MCP servers—ideal for individuals, small teams, or internal company use. With Cloud Run, you can deploy containerized MCP servers with minimal setup, automatic scaling, and built-in authentication.

### High-Level Architecture

Here’s how the recommended GCP architecture works:

1. **Artifact Registry:**
   Store your MCP server Docker images securely.

2. **Cloud Run:**
   Deploy your MCP server as a fully managed, containerized service. Cloud Run handles scaling, HTTPS, and networking for you.

3. **Authentication:**
   GCP provides two main authentication methods for securing your MCP server:
   - **IAM Invoker Permission:**
     Use a local Cloud Run proxy that authenticates requests with your Google account’s IAM permissions. Great for personal or team use—no extra setup required if you have the right permissions.
   - **OIDC ID Token:**
     Use a service account to generate OpenID Connect (OIDC) ID tokens for authentication. This is more flexible for automated or machine-to-machine access, and is the recommended approach for CI/CD or service integrations.

### Step-by-Step Flow

**[On Screen: Step numbers overlay on the GCP architecture diagram]**

1. Build and push your MCP server Docker image to Artifact Registry.
2. Deploy the image to Cloud Run, setting environment variables for secrets (e.g., API keys).
3. Secure the Cloud Run service by requiring authentication (`--no-allow-unauthenticated`).
4. For local development or team use, run a Cloud Run proxy (`gcloud run services proxy ...`)—this injects your IAM credentials into requests.
5. For automated access, configure a service account and use Google’s libraries to fetch an OIDC ID token, which is sent as a Bearer token in the Authorization header.
6. The MCP server validates the token and processes the request.

### Key Benefits

- **Simplicity:**
  Deploy and scale with almost zero infrastructure management.
- **Security:**
  Built-in HTTPS, IAM, and OIDC authentication.
- **Cost-Effective:**
  Pay only for what you use—great for individuals and small teams.
- **Easy Integration:**
  Works seamlessly with Google’s developer tools and CI/CD pipelines.

### Best Practices & Recommendations

- Use IAM Invoker Permission for quick, secure access in personal or team settings.
- Use OIDC ID tokens with service accounts for automated or production workflows.
- Always set `--no-allow-unauthenticated` to require authentication for your Cloud Run service.
- Store secrets in environment variables, not in code or images.

**[On Screen: “GCP Best Practice: Use Cloud Run for simple, secure MCP hosting. Choose IAM or OIDC auth based on your use case.”]**

---

## Remote Server Deployment: AWS

**[On Screen: AWS architecture diagram – highlight CloudFront, Cognito, MCP Auth Service, Fargate, Lambda, DynamoDB]**

Let’s dive into how you can deploy a remote MCP server on AWS, following the official AWS guidance.

### Why AWS for MCP?

AWS offers a robust, scalable, and secure environment for running MCP servers in production. With managed services like Fargate, Lambda, Cognito, and DynamoDB, you can build a highly available and secure MCP deployment without managing infrastructure manually.

### High-Level Architecture

Here’s how the recommended AWS architecture works:

1. **User & MCP Client:**
   The user interacts with the MCP client, which sends requests to the cloud.

2. **Amazon CloudFront & AWS WAF:**
   All incoming traffic is routed through Amazon CloudFront (for global distribution and caching) and AWS WAF (for web application firewall protection).

3. **Application Load Balancer (ALB):**
   Requests are forwarded to an ALB inside a Virtual Private Cloud (VPC), which directs traffic to the appropriate backend services.

4. **MCP Auth Service (MAS):**
   Authentication and authorization are handled by a dedicated MCP Auth Service, which integrates with Amazon Cognito for user management and authentication flows.

5. **Amazon Cognito:**
   Cognito provides OAuth 2.1-compliant authentication, user pools, and issuing the token. The user authenticates via Cognito, which returns access tokens to the client.

6. **MCP Server(s):**
   The actual MCP servers run on AWS Fargate (for containerized workloads) or AWS Lambda (for serverless deployments). These servers are responsible only for serving MCP resources and tools—they do not handle authentication logic directly.

7. **Amazon DynamoDB:**
   Used for storing persistent data, such as user sessions, tokens, or application state.

8. **Other AWS Services:**
   The architecture can also leverage Amazon ECR (for container images), CloudWatch (for logging and monitoring), Secrets Manager, and Parameter Store (for secure configuration).

### Step-by-Step Flow

**[On Screen: Step numbers overlay on the architecture diagram]**

1. The user initiates a request from the MCP client.
2. The request passes through CloudFront and WAF for security and routing.
3. The ALB directs the request to the MCP Auth Service (MAS) if authentication is required.
4. MAS interacts with Amazon Cognito to authenticate the user and obtain tokens.
5. The user completes authentication via Cognito (browser-based or in-app).
6. MAS stores or retrieves session data from DynamoDB as needed.
7. Once authenticated, the ALB forwards authorized requests to the MCP server(s) running on Fargate or Lambda.
8. The MCP server processes the request and returns the response to the client.

### Key Benefits

- **Separation of Concerns:**
  Authentication and resource serving are handled by separate components (MAS/Cognito vs. MCP server), keeping your MCP server lightweight and secure.

- **Scalability:**
  Fargate and Lambda allow you to scale MCP servers automatically based on demand.

- **Security:**
  AWS WAF, Cognito, and managed secrets ensure your deployment is protected against common threats.

- **Observability:**
  CloudWatch provides centralized logging and monitoring for all components.

### Best Practices & Recommendations

- Always use Amazon Cognito (or another dedicated OAuth provider) for authentication—never build auth logic into your MCP server.
- Use Fargate for containerized MCP servers, or Lambda for event-driven/serverless workloads.
- Store secrets and configuration in AWS Secrets Manager and Parameter Store.
- Monitor and log all activity with CloudWatch for security and troubleshooting.

**[On Screen: “AWS Best Practice: Keep MCP server stateless and lightweight. Delegate auth to Cognito or MAS.”]**

---

## Inspecting Low-Level Client-Server Communication

**[On Screen: Terminal window – running MCP Inspector and server]**

In this next section, let’s get hands-on and look at the low-level communication between the MCP client and server using the MCP Inspector.

First, spin up the inspector using the command line:

- Run `npx model-context-protocol inspector` to launch the Inspector UI. This will start a frontend on port 6274.

Next, open a new terminal and start your MCP server:

- Run `uv run server-dev.py` to launch the server at `localhost:8000/mcp` for streamable HTTP connections.

Once the server is running, copy the session token from the proxy server terminal and paste it into the Inspector UI, then click Connect.

If you see an error like "No proxy authentication is required," check the terminal for the correct session token from the proxy server. The Inspector UI (port 6274) connects to the proxy server running on `localhost:6277`. You’ll need to provide the correct proxy session token for authentication.

When the client sends a request, it first reaches the proxy server, which then communicates with the MCP server. Once connected, you can click on "List Tools" in the Inspector to see all available tools, just like before.

**[On Screen: Inspector UI – List Tools, tool details, request/response payloads]**

You’ll notice the request payload follows the JSON-RPC format, with a method like `tools/list` and no extra params. The response payload lists all tools with their names, descriptions, and input schemas.

Let’s try calling a tool, such as `get_page`. The request method will be `tools/call`, with parameters like `getspaces` and an argument (e.g., 25 to limit the number of spaces). The response payload will show the results as expected.

This demonstrates the MCP protocol in action. To dig deeper, you can inspect the underlying HTTP communication. The MCP protocol sits on top of HTTP, so you can use Chrome DevTools or your browser’s network inspector to see the actual HTTP requests and responses.

For example, you’ll see the client making a POST request to `/mcp` with a JSON-RPC 2.0 payload. If you disconnect, a DELETE request is sent from the client to the proxy server. Reconnecting triggers a health check (GET request) followed by an initialization POST request.

---

## The MCP Gateway: Anthropic’s Latest Innovation

**[On Screen: “MCP Gateway” logo, diagram showing gateway between clients and multiple MCP servers]**

Before we wrap up, let’s briefly talk about the latest concept introduced by the Anthropic team based on their experience building internal remote MCP servers: the MCP Gateway.

The MCP Gateway is designed to sit in front of all your MCP servers, acting as a unified entry point for all client connections. Instead of having every client connect directly to multiple MCP servers—each handling its own authentication, rate limiting, and observability—the Gateway centralizes these responsibilities.

### Key Roles of the MCP Gateway

- **Auth Management:** Handles authentication and authorization for all incoming connections, so individual MCP servers can stay lightweight.
- **Rate Limiting:** Enforces usage limits and protects backend resources from abuse.
- **Observability:** Provides centralized logging, monitoring, and analytics for all MCP traffic.

With this setup, the MCP Gateway becomes the single connection point for a wide range of clients—whether it’s Cloud AI, Slack bots, or any other internal tools. It routes requests to the appropriate MCP server, reducing duplication and streamlining management.

This architecture not only simplifies operations but also improves security and scalability by centralizing control over all MCP traffic.

**[On Screen: “Best Practice: Use an MCP Gateway to centralize auth, rate limiting, and monitoring for all MCP servers.”]**

---

**[On Screen: Outro animation, subscribe and like buttons]**

Alright guys, that’s the end of this third episode of MCP From Zero to Hero. Hope you enjoyed it, please click on subscribe and like to support the content. See you next time!
