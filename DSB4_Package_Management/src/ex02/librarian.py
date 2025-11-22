import sys
import subprocess
import os
import shutil

def check_env():
    if sys.prefix == sys.base_prefix:
        # print("The script isn't launched in a virtual environment.")
        raise Exception("The script isn't launched in a virtual environment.")
    else:
        print(f"The script is launched in a virtual environment.")

def install_libraries(packages):
    for package in packages:
        subprocess.run([sys.executable, "-m", "pip", "install", package])

def output_packages():
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=subprocess.PIPE)
    lines = result.stdout.decode().splitlines()
    print("Installed libraries:")
    for line in lines:
        print(line)
    with open("requirements.txt", "w") as f:
        f.write("\n".join(lines))



def archive_env(source):

    shutil.make_archive(base_name="./marjoraf_env", format='gztar', root_dir=source)

if __name__ == "__main__":
    try:
        # check_env()
        packages = ['six==1.14.0', 'soupsieve==2.0', 'termgraph==0.2.0', 'wcwidth==0.1.9', 'zipp==3.1.0']
        install_libraries(packages)
        output_packages()
        archive_env("../ex00/marjoraf")
    except Exception as e:
        print(e)