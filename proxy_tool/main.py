from app import create_app

app = create_app()

# 启动
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)
