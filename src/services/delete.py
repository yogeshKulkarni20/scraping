import os
import shutil


def delete():
    shutil.rmtree("data")
    shutil.rmtree("logs")
