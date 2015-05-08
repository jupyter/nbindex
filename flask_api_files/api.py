#!python 

#following this tutorial: http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

import elasticsearch
from elasticsearch import Elasticsearch
from jsmin import jsmin
from flask import abort, Flask, jsonify, make_response, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['PROPAGATE_EXCEPTIONS'] = True



dummydata = [
    {
        'nbformat':3,
        'cell_type':'code',
        'collapsed': False
    },

    {
        'cell_type':'heading',
        'level':1,
    }
]

es = Elasticsearch()



class IndexAPI(Resource):

    @staticmethod
    def put(index_name):
        """
        uses elasticsearch wrapper to create an index.

        :param index_name: string in quotes
        :return: status
        """
        try:
            es.indices.create(index=index_name)
        except elasticsearch.RequestError as re:
            return get_response

    @staticmethod
    def get():
        """
        uses make_response to convert to html (easier to read).

        :return: list of indices with their number of shards, size(b) and status (red, green, yellow)

        """
        return make_response(es.cat.indices().replace('\n','<br />'))

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify(error, 404))

api.add_resource(IndexAPI, '/data/', endpoint='database')


class MappingAPI(Resource):

    @staticmethod
    def get(index_name, doc_type):
        """
        uses elasticsearch wrapper.

        :param index_name: string in quotes, doc_type, string in quotes
        :return: mapping, or error status
        """
        try:
            es.indices.get_mapping(index=index_name, doc_type=doc_type)
        except elasticsearch.RequestError as re:
            return re

    @staticmethod
    def put(mapfile, index_name, doc_type):
        """
        uses elasticsearch wrapper.

        note that the index must already exist to be able to put_mapping in it.

        :param mapfile: json datatypes template, top level is the doc_type
        :param index_name: string in quotes
        :param doc_type: string in quotes
        :return: currently: nothing unless error
        """
        with open(mapfile, 'r') as map:
            body = jsmin(map.read())

            try:
                es.indices.put_mapping(index=index_name, doc_type=doc_type, body=body)
            except elasticsearch.RequestError as re:
                return re

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify(error, 404))

api.add_resource(MappingAPI, '/mappings/', endpoint='maps')


class NotebookAPI(Resource):

    @staticmethod
    def put():
        """
        this will be used to bulk upload notebooks.

        :return:
        """
        if not request.json or not 'title' in request.json:
            abort(400)


    @staticmethod
    def get(nb_id):
        """
        To get notebooks by id.

        :param nb_id:
        :return:
        """
        nb = [nb for nb in nbindex if nb['id']==nb_id]
        if len(task) ==0:
            abort(404)
        return jsonify({'dummydata': dummydata[0]})

    # @app.route('/', methods=['POST'])
    # def submit_notebook():
    #     """
    #     Might be used to add one notebook at a time.
    #     """
    #     if not request.json or not 'title' in request.json:
    #         abort(400)
    #     nb = {
    #         'id': nbindex[-1]['id']+1,
    #         'title': request.json['title'],
    #         'description': request.json.get('description', "")
    #     }
    #     notebooklist.append(nb)
    #     return jsonify({'dummydata': dummydata}), 201

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Notebook not found'}), 404)

api.add_resource(NotebookAPI, '/notebooks/', endpoint='notebooks')




class OtherAPI(Resource):

    @app.route('/nbindex/api/v1.0/notebooks/<int:nb_id>', methods=['DELETE'])
    def delete_nb(nb_id):
        """
        Not sure we actually want to expose this.

        :param nb_id:
        :return: response
        """
        nb = [nb for nb in nbindex if nb['id']==nb_id]
        if len(nb)==0:
            abort(404)
        notebooklist.remove(nb[0])
        return jsonify({'result': True})



#     @app.route("/")
#     def hello(self):
#         """
#         For testing.
#
#         :return:
#         """
#         return "Hello, World!"
#
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
# api.add_resource(HelloWorld, '/')

#in case of trouble:


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


#logging

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('error.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

    from logging import Formatter
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

if __name__ == '__main__':
    app.run(debug=True)

