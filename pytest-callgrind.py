if __name__ == '__main__':
    from subprocess import call, check_output
    import subprocess
    import sys
    import os
    import sysconfig

    if "'--with-valgrind'" not in sysconfig.get_config_var('CONFIG_ARGS'):
        print("Python should be compiled with the '--with-valgrind' flag")
        sys.exit(1)
    # Include current env path

    env = {
        **os.environ,
        "PYTHONMALLOC": "malloc",
        "PYTHONHASHSEED": "0",
        "PYTHONPATH": os.path.dirname(os.path.abspath(__file__)),
    }
    arch = check_output(["uname", "-m"], env=env).decode("utf8").strip()
    os.makedirs(".benchmarks", exist_ok=True)
    cmd = [
        "setarch",
        arch,
        "-R",
        "valgrind",
        "-q",
        "--tool=callgrind",
        "--I1=32768,8,64",
        "--D1=32768,8,64",
        "--LL=8388608,16,64",
        "--instr-atstart=no",
        "--compress-strings=no",
        "--combine-dumps=yes",
        f"--callgrind-out-file=.benchmarks/pytest-callgrind.out",
        sys.executable,
        "-m",
        "pytest",
        *sys.argv[1:],
    ]
    r = subprocess.call(cmd, env=env)
    exit(r)
