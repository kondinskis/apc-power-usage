from setuptools import setup

setup(
    name="APC Power Usage",
    version="0.0.1",
    packages=["apc"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask>=2.0.1", "SQLAlchemy>=1.4.25"],
)
