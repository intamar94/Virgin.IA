"""Vercel entrypoint for the Virgin.IA laboratory."""

from virgin_ia.webapp import Handler

# Vercel's Python runtime can use a BaseHTTPRequestHandler subclass directly.
handler = Handler
