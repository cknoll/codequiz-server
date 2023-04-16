from .widgets import BuilderTextArea
version = (1, 0, 0)


def get_version():
    """returns a pep compliant version number"""
    return '.'.join(str(i) for i in version)
