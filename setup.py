from distutils.core import setup

setup(
    name='django-query-parameters',
    version='0.2.2',
    author='Jean-Marc Skopek',
    author_email='jean-marc@skopek.ca',
    packages=['query_parameters','query_parameters.templatetags'],
    scripts=[],
    url='https://github.com/jskopek/django-query-parameters',
    license='LICENSE',
    description='Django templatetags to simplify creating, updating, and removing query parameters from querystring',
    long_description=open('README.rst').read(),
    install_requires=['Django >= 1.4']
)

        
