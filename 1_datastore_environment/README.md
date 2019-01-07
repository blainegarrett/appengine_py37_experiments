# AppEngine Python 3.7 Experiments 1: Datastore and Functional Testing


# Install
cd appengine_py37_experiments/1_datastore_environment
mkvirtualenv -p ~/.pyenv/versions/3.7.0/bin/python -a . lessons1
workon lessons1
make install

# Running App with Datastore Emulator
```
make dev
```

Next, *in a new terminal* run the following to start the emulator
```
make dev-env
```

Finally Open `http://localhost:8080` in your browser.  

# Running Integration Tests with Datastore Emulator
First, be sure that the emulator isn't running - specifically not still running from the above `make local-env` command. There should be nothing running at `http://localhost:8081/`

First, *in a new terminal* run the following to start the emulator
```
make test-env
```

Finally, run the integration tests
```
make integrations
```
