def application(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])

    return [b"This is ebenv-test project. There is nothing to do here."]
