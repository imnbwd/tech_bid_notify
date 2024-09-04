from flask import Flask, request, jsonify, Response

app = Flask(__name__)

result_dict = {}


@app.route('/notify', methods=['POST'])
def notify() -> None:
    # 先检查请求体是否为JSON格式，并且是否包含'task_id'
    if request.is_json:
        data = request.get_json()  # 获取JSON数据
        task_id = data.get("task_id")  # 使用get方法获取task_id，若不存在则返回None或指定默认值
        if task_id is not None:
            # 在此处理task_id的逻辑
            result_dict[task_id] = data
            print(data)
            return jsonify({"status": "success", "task_id": task_id})

        else:
            # 处理task_id不存在的情况
            return jsonify({"status": "error", "message": "task_id is missing"}), 400
    else:
        # 处理请求不是JSON格式的情况
        return jsonify({"status": "error", "message": "Invalid JSON request"}), 400


@app.route('/query', methods=['GET'])
def query() -> Response:
    task_id = request.args.get("task_id")
    if task_id is None:
        return jsonify({"status": "error", "message": "task_id is missing"}), 400

    result = result_dict.get(task_id, None)
    return jsonify({"status": "success", "result": result})


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True, port=5500)
