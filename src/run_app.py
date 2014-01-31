"""
Start the server and run the app
"""

from klein import run, route


@route('/')
def home(request):
    return "Hello World"


if __name__ == '__main__':
    run("localhost", 8089)
