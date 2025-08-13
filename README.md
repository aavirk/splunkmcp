# Splunk ITSI MCP Server

Splunk ITSI MCP is a Python-based MCP (Model Context Protocol) server for Splunk IT Service Intelligence (ITSI). This server provides comprehensive tools for querying the Splunk API to monitor service health, execute searches, and manage your IT operations monitoring infrastructure.

## Features

- **Service Health Monitoring** - Get real-time service health data from ITSI Service Analyzer
- **Splunk Search** - Execute SPL (Splunk Processing Language) queries directly
- **Index Management** - List and explore all configured Splunk indexes
- **Health Visualization** - Generate interactive HTML charts for service health metrics
- **Core Splunk Access** - Direct access to Splunk's powerful search and analytics capabilities
- **Simple and extensible MCP server implementation**

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/aavirk/splunkmcp.git
cd splunkmcp
```

2. **Create a virtual environment and activate it:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file in the project directory:**

Copy the example environment file:

```bash
cp .env-example-splunk .env
```

5. **Update the `.env` file with your Splunk credentials:**
```
SPLUNK_URL="https://your-splunk-instance.com"
SPLUNK_USERNAME="your-username"
SPLUNK_PASSWORD="your-password"
```

## Usage with Claude Desktop

1. **Configure Claude Desktop to use this MCP server:**
   - Open Claude Desktop
   - Go to Settings > Developer > Edit Config
   - Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "Splunk_ITSI_MCP": {
      "command": "/path/to/your/splunk-itsi-mcp/.venv/bin/python",
      "args": [
        "/path/to/your/splunk-itsi-mcp/splunk_mcp_server.py"
      ]
    }
  }
}
```

   - Replace the paths above to reflect your local environment

2. **Restart Claude Desktop**

3. **Interact with Claude Desktop** - you can now ask questions about your Splunk environment such as:
   - "What's the current health of all ITSI services?"
   - "Show me the service analyzer view"
   - "Search for errors in the last hour"
   - "List all available Splunk indexes"
   - "Create a visualization of service health scores"
   - "Run a search for failed login attempts"

## Available Functions

The MCP server provides the following functions:

### Service Monitoring
- `get_service_analyzer_view` - Retrieve the high-level service health view from ITSI Service Analyzer

### Search and Analytics
- `run_splunk_search` - Execute a Splunk search query (SPL) and return results

### Index Management
- `get_splunk_indexes` - Retrieve a list of all configured indexes in Splunk

### Visualization
- `visualize_service_health` - Generate an HTML bar chart visualizing health scores of all ITSI services

## Example Queries

Here are some example interactions you can have with Claude Desktop:

- **Service Health**: "Show me the current health status of all ITSI services"
- **Search Execution**: "Search for all error events in the main index from the last 24 hours"
- **Index Discovery**: "What indexes are available in my Splunk instance?"
- **Visualization**: "Create a bar chart showing service health scores"
- **Complex Searches**: "Find all authentication failures in the last week and show me the top 10 users"

## Security

- Store your Splunk credentials securely in the `.env` file
- Never commit credentials to version control
- The `.env` file should be added to `.gitignore`
- Consider using token-based authentication for production environments
- SSL certificate verification is disabled by default for self-signed certificates

## Troubleshooting

If you encounter issues:

1. **Verify your Splunk credentials are correct** - Check username, password, and URL in `.env`
2. **Check network connectivity** to your Splunk instance
3. **Ensure your user account has appropriate permissions** in Splunk/ITSI
4. **Verify ITSI is installed** and properly configured on your Splunk instance
5. **Check the Splunk management port** (default is 8089) is accessible
6. **Review the console output** - Debug information is printed to stderr

### Common Issues

- **Authentication Failed**: Double-check credentials and ensure the user has API access
- **Connection Timeout**: Verify the Splunk URL and port accessibility
- **Missing ITSI Data**: Ensure ITSI app is installed and the user has appropriate permissions
- **SSL Errors**: For self-signed certificates, SSL warnings are suppressed by default

## Requirements

- Python 3.8 or higher
- Splunk instance with ITSI installed
- Splunk user account with appropriate permissions
- Network access to Splunk management port (8089)

## Dependencies

See `requirements.txt`:
- `fastmcp` - MCP server framework
- `python-dotenv` - Environment variable management
- `requests` - HTTP client library
- `urllib3` - HTTP library with SSL support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
