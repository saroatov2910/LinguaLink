import uvicorn

if __name__ == "__main__":
    # Note: The path to the app is now 'src.main_server:app' because we are running from the root directory.
    uvicorn.run("src.main_server:app", host="127.0.0.1", port=8000, reload=True)
