import os
from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

PRESTASHOP_URL = os.environ.get("PRESTASHOP_URL", "https://saporicampani.it")
PRESTASHOP_API_KEY = os.environ.get("PRESTASHOP_API_KEY")

@app.route("/health",methods=["GET"])
def health():
    return jsonify({"status": "ok"})
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "service": "Saporicampani PrestaShop Bridge"
    })



     

from mcp.server import MCPServer
mcp=MCPServer("saporicampani")
@mcp.tool()    
def get_product_mcp(product_id: int):
    if not PRESTASHOP_API_KEY:
        return {"error": "PRESTASHOP_API_KEY non configurata"}

    url = f"{PRESTASHOP_URL}/api/products/{product_id}"
    response = requests.get(
        url,
        params={"output_format": "JSON"},
        auth=HTTPBasicAuth(PRESTASHOP_API_KEY, ""),
        timeout=30
    )   
    return {"status_code": response.status_code, "content_type": response.headers.get("Content-Type"
                                                                                     
                                                                                     ), "body": response.text}
@mcp.tool()
def test_prestashop():
    url = f"{PRESTASHOP_URL}/api/products/64"
    response = requests.get(
        url,
        params={"output_format":"json"},
        auth=HTTPBasicAuth(PRESTASHOP_API_KEY, ""),
        timeout=30
)
    return {"ok":response.status_code == 200,"status_code":response.status_code}
    












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



@mcp.tool()
def update_product(product_id: int, field: str, value: str):
    if not PRESTASHOP_API_KEY:
        return {"error": "PRESTASHOP_API_KEY non configurata"}

    url = f"{PRESTASHOP_URL}/api/products/{product_id}"

    # PrestaShop supports PATCH for partial resource updates.
    # This avoids resending required fields (for example price) when
    # only one product field needs to be changed.
    import xml.etree.ElementTree as ET
    root = ET.Element("prestashop")
    product = ET.SubElement(root, "product")
    ET.SubElement(product, "id").text = str(product_id)
    ET.SubElement(product, field).text = str(value)
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    response = requests.patch(
        url,
        data=xml,
        auth=HTTPBasicAuth(PRESTASHOP_API_KEY, ""),
        headers={"Content-Type": "application/xml"},
        timeout=30
    )

    return {
        "ok": response.status_code in (200, 201),
        "status_code": response.status_code,
        "response": response.text
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    mcp.run(transport="streamable-http",host="0.0.0.0", port=port)
    
