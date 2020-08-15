from setuptools import setup, find_packages

def read(filename):
    return [req.strip() for req in open(filename).readlines()]

setup(
    name="codesevenapi",
    version="0.1.0",
    description="API para o processo seletivo na empresa Code7.",
    packages=find_packages(),
    include_packages=True,
    install_requires=read('requirements.txt'),
    extra_requires={"dev": "requirements-dev.txt"},

)
