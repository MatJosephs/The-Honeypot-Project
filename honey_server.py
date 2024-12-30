from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
from datetime import datetime
import os

class BashCommandServerHandler(SimpleHTTPRequestHandler):
    server_version = "BashCommandServer/1.0"  # Custom server header value

    def send_custom_headers(self):
        """Send custom headers for all responses."""
        self.send_header("Server", self.server_version)
        self.send_header("Content-type", "text/html")

    def do_GET(self):
        """Serve the HTML form."""
        if self.path == "/":
            self.send_response(200)
            self.send_custom_headers()
            self.end_headers()

            # HTML form
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Run bash commands</title>
            </head>
            <body>
                <h1>Enter your bash command:</h1>
                <form action="/submit" method="POST">
                    <input type="text" name="command" required>
                    <button type="submit">Submit</button>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        """Handle form submissions."""
        if self.path == "/submit":
            # Get the content length and read the POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse the command from the form data
            command = urllib.parse.parse_qs(post_data).get('command', [''])[0]

            # Gather additional information
            ip_address = self.client_address[0]  # Client IP address
            user_agent = self.headers.get("User-Agent", "Unknown")  # User-Agent header
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current datetime

            # Log the received command with additional information
            with open("../command_log.txt", "a") as log_file:
                log_file.write(
                    f"[{timestamp}] IP: {ip_address}, Command: '{command}', User-Agent: '{user_agent}'\n"
                )

            # Respond with a confirmation page
            self.send_response(200)
            self.send_custom_headers()
            self.end_headers()

            confirmation_page = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Command Received</title>
            </head>
            <body>
                <h1>Command received successfully!</h1>
                <a href="/">Go back</a>
            </body>
            </html>
            """
            self.wfile.write(confirmation_page.encode("utf-8"))

if __name__ == "__main__":
    os.chdir("honey")
    server_address = ("", 80)
    httpd = HTTPServer(server_address, BashCommandServerHandler)
    print("Serving on port 80...")
    httpd.serve_forever()
