import nox
locations = "bot", "main.py", "cloud.py", "noxfile.py"


@nox.session
def tests(session):
    session.install('pytest')
    session.run('pytest')


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
