import subprocess
import shlex


def echo_and_run(cmd: list[str]) -> None:
    print(shlex.join(cmd))
    subprocess.call(cmd)


def rebuild():
    with open("src_c/geometry.c", "a") as f:
        f.write("\n")

    echo_and_run(["python", "setup.py", "format"])

    echo_and_run(["pip", "install", "."])

    echo_and_run(["python", "test/test_circle.py"])
    echo_and_run(["python", "test/test_line.py"])
    echo_and_run(["python", "test/test_polygon.py"])


rebuild()
import examples.raycast
