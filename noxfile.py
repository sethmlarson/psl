import os

import nox

source_files = ("psl/", "test_psl.py", "build.py", "setup.py", "noxfile.py")


@nox.session(reuse_venv=True)
def format(session):
    session.install("autoflake", "black", "flake8", "isort", "seed-isort-config")

    session.run("autoflake", "--in-place", "--recursive", *source_files)
    session.run("seed-isort-config", "--application-directories=psl")
    session.run(
        "isort",
        "--project=psl",
        "--multi-line=3",
        "--trailing-comma",
        "--force-grid-wrap=0",
        "--combine-as",
        "--line-width=88",
        "--recursive",
        "--apply",
        *source_files,
    )
    session.run("black", "--target-version=py36", *source_files)

    lint(session)


@nox.session(reuse_venv=True)
def lint(session):
    session.install("black", "flake8", "mypy")

    session.run("black", "--check", "--target-version=py36", *source_files)
    session.run("flake8", "--max-line-length=88", "--ignore=W503,E203", *source_files)
    session.run("mypy", "--strict", "psl/")


@nox.session(reuse_venv=True)
def build(session):
    session.install("urllib3", "idna")

    session.run("python", "build.py")


@nox.session(reuse_venv=True)
def test(session):
    session.install("urllib3", "idna", "pytest")
    session.install(".")

    session.run("python", "-m", "pytest", "test_psl.py")


@nox.session(reuse_venv=True)
def deploy(session):
    session.install("twine")

    if os.path.isdir("dist"):
        session.run("rm", "-rf", "dist/*")

    session.run("python", "setup.py", "build", "sdist", "bdist_wheel")

    if os.getenv("PYPI_TOKEN"):
        username = "__token__"
        password = os.getenv("PYPI_TOKEN")
    else:
        username = os.environ["PYPI_USERNAME"]
        password = os.environ["PYPI_PASSWORD"]

    session.run(
        "python",
        "-m",
        "twine",
        "upload",
        "--skip-existing",
        "dist/*",
        f"--username={username}",
        f"--password={password}",
        success_codes=[0, 1],
    )
