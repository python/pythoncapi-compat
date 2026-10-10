import subprocess
import sys


def _run_command(cmd, **kw):
    sys.stdout.flush()
    sys.stderr.flush()

    kw['shell'] = False
    if hasattr(subprocess, 'run'):
        proc = subprocess.run(cmd, **kw)
    else:
        proc = subprocess.Popen(cmd, **kw)
        try:
            proc.communicate()
            proc.wait()
        except:
            proc.kill()
            proc.wait()
            raise
    return proc


def run_command(cmd, **kw):
    proc = _run_command(cmd, **kw)
    exitcode = proc.returncode
    if exitcode:
        sys.exit(exitcode)


def get_output(cmd, **kw):
    # Legacy for text=True
    kw['universal_newlines'] = True
    proc = _run_command(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        **kw)
    return (proc.returncode, proc.stdout)
