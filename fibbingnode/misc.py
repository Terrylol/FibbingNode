import os
import sys
from time import sleep
from fibbingnode import log


def require_cmd(cmd, help_str=None):
    """
    Ensures that a command is available in $PATH
    :param cmd: the command to test
    :param help_str: an optional help string to display if cmd is not found
    """
    # Check if cmd is a valid absolute path
    if os.path.isfile(cmd):
        return
    # Try to find the cmd in each directory in $PATH
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe = os.path.join(path, cmd)
        if os.path.isfile(exe):
            return
    log.error('[%s] is not available in $PATH', cmd)
    if help_str:
        log.error(help_str)
    sys.exit(1)


def need_root():
    """
    Ensures that the program is run as root
    """
    if os.getuid() != 0:
        log.error('%s: Must be run as root!', sys.argv[0])
        sys.exit(1)


def post_delay(amount):
    """
    Sleep some time after executing the function
    :param amount: the amount of seconds to wait
    :return: the return value of the function
    """
    def inner(f):
        def inner_f(*args, **kwargs):
            r = f(*args, **kwargs)
            sleep(amount)
            return r
        return inner_f
    return inner


def force(f, *args, **kwargs):
    """
    Force the execution of function and log any exception
    :param f: the function to execute
    :param args: its arguments
    :param kwargs: its kw-arguments
    :return: the return value of f is any, or None
    """
    try:
        return f(*args, **kwargs)
    except Exception as e:
        log.exception(e)
        return None


def dump_threads():
    """
    Shouldn't be used except for debugging purpose (e.g. find deadlocks)
    """
    import sys
    import traceback

    print >> sys.stderr, "\n*** STACKTRACE - START ***\n"
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# ThreadID: %s" % threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))

    for line in code:
        print >> sys.stderr, line
    print >> sys.stderr, "\n*** STACKTRACE - END ***\n"