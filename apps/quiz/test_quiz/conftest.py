import os

if os.getenv("PYTEST_IPS", None) == "True":

    import ipydex

    def pytest_runtest_setup(item):
        print("This invocation of pytest is customized")


    def pytest_exception_interact(node, call, report):
        ipydex.ips_excepthook(call.excinfo.type, call.excinfo.value, call.excinfo.tb, frame_upcount=0)
