import uvicorn

def start():
    """
    This function is the entry point that uvicorn will use to run the app.
    It's equivalent to running `uvicorn datatrac.api.main:app --reload`
    from the command line.
    """
    uvicorn.run(
        "datatrac.api.main:app", 
        host="localhost", 
        port=8000, 
        reload=True
    )

if __name__ == "__main__":
    start()