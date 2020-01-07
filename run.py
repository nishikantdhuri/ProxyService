from app import create_app
app = create_app()

@app.errorhandler(404)
def handle_error(e):
    return "Page Not Found"

if __name__ == '__main__':
    app.run()