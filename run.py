"""
  Created by PyCharm.
  User: Liujianhan
  Date: 2019/3/28
  Time: 16:10
 """

from flaskblog import create_app

__author__ = 'liujianhan'

app = create_app()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
