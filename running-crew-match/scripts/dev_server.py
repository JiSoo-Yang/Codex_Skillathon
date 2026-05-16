#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from crew_matcher import DEFAULT_DATA_PATH, match_crews


class RunningCrewHandler(BaseHTTPRequestHandler):
    server_version = "RunningCrewMatchDemo/0.1"

    def _write_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._write_json({"status": "ok", "mode": "demo", "data_source": self.server.data_path})
            return
        if self.path == "/":
            self._write_json(
                {
                    "service": "running-crew-match-demo",
                    "endpoints": ["GET /health", "POST /match"],
                    "data_source": self.server.data_path,
                }
            )
            return
        self._write_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/match":
            self._write_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._write_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
            return

        result = match_crews(
            region=payload.get("region", ""),
            day=payload.get("day", ""),
            time=payload.get("time", ""),
            level=payload.get("level", ""),
            goal=payload.get("goal", ""),
            notes=payload.get("notes", ""),
            limit=int(payload.get("limit", 5)),
            data_path=self.server.data_path,
        )
        self._write_json(result)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the running crew match demo API.")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    parser.add_argument("--data", default=os.environ.get("RUNNING_CREW_MATCH_DATA_PATH", str(DEFAULT_DATA_PATH)))
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), RunningCrewHandler)
    server.data_path = args.data
    print(f"RunningCrewMatch demo server on http://{args.host}:{args.port}")
    print(f"Using data source: {args.data}")
    server.serve_forever()


if __name__ == "__main__":
    main()
