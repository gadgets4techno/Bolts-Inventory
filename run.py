# I just wanted to test a commit 

from inventory import create_app
import os

app = create_app()
port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
        app.run(host="0.0.0.0",port=port,debug=True)