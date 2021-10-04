from setuptools import setup

setup(
    name="APC Power Usage",
    version="0.1.5",
    author="Stefan Kondinski",
    description="APC Power Usage is an application which shows power consuption overtime for UPS units manufactured by APC.",
    url="https://github.com/kondinskis/apc-power-usage",
    project_urls={
        "Bug Tracker": "https://github.com/kondinskis/apc-power-usage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    packages=["apc"],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask>=2.0.1", "SQLAlchemy>=1.4.25"],
)
