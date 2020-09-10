from database.models import *

from flask import Flask, jsonify, request

app = Flask(__name__)
pricing_objs = {}


@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({
        'error': 'Bad Request'
    })
    return response


@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({
        'error': 'Internal Server Error'
    })
    return response


@app.errorhandler(401)
def unauthorized_error(error):
    response = jsonify({
        'error': 'Unauthorized User Access'
    })
    return response


@app.route('/xrs/eth_passthrough/requestprojectid', methods=['POST'])
def requestprojectid():
    payload = request.json
    print('payload: {}'.format(payload))
    #TODO: handle payment, for now lets just create project id, assign some value for api requests
    # need to gen project-id, project-id, api-secret, add to db
    addprojectid_db()
    return jsonify(payload)

@db_session
def addprojectid_db():
    #
    print('add to db')

@app.route('/xrs/eth_passthrough/<project_id>', methods=['POST'])
def handlerequest(project_id):
    #request_json = request.json
    print('project_id: {}'.format(project_id))
    return project_id


def main():
    app.run(host='0.0.0.0', port=8887)


if __name__ == '__main__':
    main()

