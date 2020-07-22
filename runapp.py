from melbviz.app import app


if __name__ == "__main__":
    app.run_server(
        debug=True, dev_tools_prune_errors=False, dev_tools_silence_routes_logging=True
    )
