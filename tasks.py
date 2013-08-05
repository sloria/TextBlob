from invoke import run, task

@task
def test():
    run("python run_tests.py", pty=True)

@task
def deps():
    print("Vendorizing nltk...")
    run("rm -rf text/nltk")
    run("git clone https://github.com/nltk/nltk.git")
    run("mv nltk/nltk text/")
    run("rm -rf nltk")