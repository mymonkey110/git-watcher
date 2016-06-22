from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='git-watcher',
    version='0.1',
    keywords=('git', 'git-watcher', 'github', 'blog'),
    url='https://github.com/mymonkey110/git-watcher',
    description="ssh host command manager tool",
    long_description=readme(),
    license='MIT License',
    install_requires=['pexpect', 'ptyprocess', 'tabulate'],
    author='Michael Jiang',
    author_email='mymonkey110@gmail.com',
    maintainer='Michael Jiang',
    maintainer_email='mymonkey110@gmail.com',
    packages=['git-watcher'],
    package_data={
    },
    platform=('Linux', 'Mac'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'sm = sm.main:main',
        ]
    }
)
