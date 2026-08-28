"""Vercel-compatible Flask adapter for the Virgin.IA laboratory."""

from flask import Flask, jsonify, request

from .auto_discovery import AutoDiscovery
from .problems import maxcut_triangle
from .webapp import HTML

app = Flask(__name__)


@app.get("/")
def home():
    return HTML


@app.get("/api")
def api_home():
    return {"service": "Virgin.IA", "status": "ok"}


@app.post("/api/run")
def run_experiment():
    try:
        payload = request.get_json(silent=True) or {}
        generations = max(1, min(20, int(payload.get("generations", 3))))
        result = AutoDiscovery().run(maxcut_triangle(), generations=generations)
        return jsonify({
            "reward": result.experiment.reward,
            "best_score": result.experiment.best_score,
            "success_probability": result.experiment.success_probability,
            "circuit_depth": result.experiment.circuit_depth,
            "strategy": result.experiment.strategy,
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
