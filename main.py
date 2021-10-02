from apc import Collector, create_app


collector = Collector()
collector.start()

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
