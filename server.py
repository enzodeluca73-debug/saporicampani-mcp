import os
from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

PRESTASHOP_URL = os.environ.get("PRESTASHOP_URL", "https://www.saporicampani.it")
PRESTASHOP_API_KEY = os.environ.get("PRESTASHOP_API_KEY")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "service": "Saporicampani PrestaShop Bridge"
    })



     

from mcp.server.fastmcp import FastMCP
mcp = FastMCP("saporicampani",stateless_http=true)
@mcp.tool()    
def get_product_mcp(product_id: int):
    return get_product(product_id)
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    if not PRESTASHOP_API_KEY:
        return jsonify({"error": "PRESTASHOP_API_KEY non configurata"}), 500

    url = f"{PRESTASHOP_URL}/api/products/{product_id}"

    response = requests.get(
        url,
        params={"output_format": "JSON"},
        auth=HTTPBasicAuth(PRESTASHOP_API_KEY, ""),
        timeout=30
    )

    return (
        response.text,
        response.status_code,
        {"Content-Type": response.headers.get("Content-Type", "application/json")}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)app.run(host="o.o.o.o", port=port)
    
