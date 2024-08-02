from setuptools import setup

setup(
    name="trends-earth-cli",
    version="1.0.3",
    description="Library to interact with trends-earth",
    author="Sergio Gordillo, Raul Requero",
    author_email="sergio.gordillo@vizzuality.com,raul.requero@vizzuality.com",
    license="MIT",
    packages=["tecli"],
    package_data={
        "": [
            "run/Dockerfile",
            "skeleton/requirements.txt",
            "skeleton/src/__init__.py",
            "skeleton/src/main.py",
        ]
    },
    install_requires=[
        "fire>=0.6.0",
        "PyYAML>=6.0.1",
        "requests>=2.32.3",
        "termcolor>=2.4.0",
        "python-dateutil>=2.9.0",
    ],
    entry_points={"console_scripts": ["trends=tecli:main"]},
    zip_safe=False,
)
