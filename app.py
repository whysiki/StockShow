# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from get_stock_data import get_price_min_tx
from extract_data import extract_data

app = Flask(__name__)
CORS(app)  # 启用CORS


@app.route("/stock", methods=["GET"])
def get_stock_info():
    # 获取股票代码
    stock_code = request.args.get("code")
    count = request.args.get("count", 0)
    if not stock_code:
        return jsonify({"error": "Stock code is required"}), 400

    # 调用 get_stock_data.py 获取股票数据
    try:
        raw_json, _ = get_price_min_tx(
            code=stock_code, minute_frequency=1, count=int(count)
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 调用 extract_data.py 提取数据
    try:
        extracted_data = extract_data(raw_json, stock_code)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 返回提取的数据
    return jsonify(extracted_data)


# if __name__ == "__main__":
# app.run(debug=True, port=5000)
