import os, environ


environ.Env.read_env(os.path.join(".env"))

env = environ.Env(
    
)