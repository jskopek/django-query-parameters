from distutils.core import setup

setup(
    name='django-query-parameters',
    version='0.1.1',
    author='Jean-Marc Skopek',
    author_email='jean-marc@skopek.ca',
    packages=['query_parameters','query_parameters.templatetags'],
    scripts=[],
    url='http://pypi.python.org/pypi/django-query-parameters',
    license='LICENSE',
    description='Django templatetags to simplify creating, updating, and removing query parameters from querystring',
    long_description=open('README.rst').read(),
    install_requires=['Django >= 1.4']
)

        
