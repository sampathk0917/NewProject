import re
from sqlite3.dbapi2 import Cursor
import sys
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Iterable


class Server(BaseHTTPRequestHandler):
    def _send_headers(self):
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            html_string = """
            <html>
            <head></head>
            <body>
                <h1>Login</h1>
                <form action="/rates" method="get">
                <label>Name:</label><br>
                <input type="text"><br>
                <label>Password:</label><br>
                <input type="password"><br>
                <input type="submit" value="Submit">
                </form>
            </body>
            """
            self.send_response(200)
            self._send_headers()
            self.wfile.write(bytes(html_string, "utf-8"))
        if re.match("/rates[?]*", self.path):
            html_string = """<html>
            <head></head>
            <h1>Exchange Rates</h1>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>USD</th>
                    <th>EUR</th>
                    <th>GBP</th>
                    <th>JPY</th>
                    <th>AUD</th>
                    <th>CAD</th>
                    <th>INR</th>
                    <th>CHF</th>
                </tr>
            """
            self.send_response(200)
            self._send_headers()
            conn = sqlite3.connect("forex.db")
            cursor = conn.cursor()
            try:
                res = cursor.execute("select * from exchange_rates;")
            except Exception as e:
                print(e)
            for i in res:
                html_string += (
                    "<tr>"
                    f"<td>{i[0]}</td>"
                    f"<td>{i[1]}</td>"
                    f"<td>{i[2]}</td>"
                    f"<td>{i[3]}</td>"
                    f"<td>{i[4]}</td>"
                    f"<td>{i[5]}</td>"
                    f"<td>{i[6]}</td>"
                    f"<td>{i[7]}</td>"
                    f"<td>{i[8]}</td>"
                    "</tr>"
                )
            html_string += "</head></html>"
            self.wfile.write(bytes(html_string, "utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Server)
    print("Starting server at :8000...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Shutting down...")
