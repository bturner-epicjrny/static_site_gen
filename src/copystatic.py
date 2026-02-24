import os
import shutil


def copy_dir_recursive(src, dst):
    # delete destination completely so copy is clean
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # recreate destination root
    os.mkdir(dst)

    _copy_contents(src, dst)


def _copy_contents(src, dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_contents(src_path, dst_path)
