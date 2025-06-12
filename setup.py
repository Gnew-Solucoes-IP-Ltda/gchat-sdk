from setuptools import setup


with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='gchat-sdk',
    version='0.0.3',
    license='MIT License',
    author='Tatianno Alves',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tferreiraalves@gmail.com',
    keywords='gchat chatbot sdk gnew',
    description=u'Gchat SDK for managing and closing conversations',
)