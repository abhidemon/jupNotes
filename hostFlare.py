from bottle import run, static_file, route
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='/Users/abhi/PycharmProjects/jupNotes/')

run(host='localhost', port=8080, debug=True)