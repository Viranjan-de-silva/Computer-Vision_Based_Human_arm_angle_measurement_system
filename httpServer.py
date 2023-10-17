from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        request_line = self.requestline
        request_line = request_line[5:(len(request_line) - 9)]
        response = f"Request : {request_line}\nHello, this is the server response!"
        self.wfile.write(response.encode('utf-8'))

        # Deposit the request into the queue
        request_queue.put(request_line)


def run_server(server_class=HTTPServer, handler_class=MyRequestHandler, port=9999):
    server_address = ('{your IP address}', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server is running on port {port}")

    # Start the server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True  # The thread will exit when the main program ends
    server_thread.start()


# Create a global queue to store incoming requests
import queue

request_queue = queue.Queue()

# Start the server in a separate thread
run_server()
