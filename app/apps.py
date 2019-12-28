from app import create_app
app = create_app()

@app.errorhandler(404)
def handle_error(e):
    return "Page Not Found"


SITE_NAME1 = 'http://127.0.0.1:81'
SITE_NAME2 = 'http://127.0.0.1:82'
curr_req=''
count=0
map_port={'81':'http://127.0.0.1:81','82':'http://127.0.0.1:82'}
states={'81':['CLOSED',0,0],'82':['CLOSED',0,0]}


if __name__ == '__main__':
    app.run()