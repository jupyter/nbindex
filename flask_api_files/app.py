#!python 

#following this tutorial: http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


from flask import abort, Flask, jsonify, make_response, request

app = Flask(__name__)

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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Notebook not found'}), 404)

@app.route('/nbindex/api/v1.0/<int:nb_id>', methods=['GET'])
def get_nb(nb_id):
    nb = [nb for nb in nbindex if nb['id']==nb_id]
    if len(task) ==0:
        abort(404)
    return jsonify({'dummydata': dummydata[0]})

@app.route('/nbindex/api/v1.0/notebooks', methods=['POST'])
def submit_notebook():
    if not request.json or not 'title' in request.json:
        abort(400)
    nb = {
        'id': nbindex[-1]['id']+1,
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }
    notebooklist.append(nb)
    return jsonify({'dummydata': dummydata}), 201

@app.route('/nbindex/api/v1.0/notebooks/<int:nb_id>', methods=['DELETE'])
def delete_nb(nb_id):
    nb = [nb for nb in nbindex if nb['id']==nb_id]
    if len(nb)==0:
        abort(404)
    notebooklist.remove(nb[0])
    return jsonify('result': True})


#def index():
#    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True)

