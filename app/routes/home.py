from app.routes import app


@app.route('/')
def main():
    return 'Main!'
