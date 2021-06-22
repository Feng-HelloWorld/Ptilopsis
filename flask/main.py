from app.app import creat_app

app = creat_app()

if __name__=="__main__":
    app.run(host='0.0.0.0',port=3003, ssl_context=('cert.pem','cert.key'))