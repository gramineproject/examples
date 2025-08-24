# Copyright (C) 2024 Gramine contributors
# SPDX-License-Identifier: BSD-3-Clause

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/hello', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
