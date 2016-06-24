from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='git-watcher',
    version='0.7',
    keywords=('git', 'git-watcher', 'github', 'blog', 'hexo', 'baidu'),
    url='https://github.com/mymonkey110/git-watcher',
    description="git watcher will rebuild your repository when you push code to github.",
    long_description=readme(),
    license='MIT License',
    install_requires=[],
    author='Michael Jiang',
    author_email='mymonkey110@gmail.com',
    maintainer='Michael Jiang',
    maintainer_email='mymonkey110@gmail.com',
    packages=['watcher'],
    package_data={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'git-watcher=watcher.main:main',
        ]
    }
)
