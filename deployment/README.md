Note: this deployment process is copied from other projects and is not yet fully adapted to the codequiz project.

issues:

- config_example.ini does not contain all keys from the real config
- collect static copies to run directory and the cp command uses the wrong path
- initial fixture contains superuser with trivial password
- there is no established way to dump the new tasks to a nice json file