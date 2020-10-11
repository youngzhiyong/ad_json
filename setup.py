from setuptools import setup
import ad_json

setup(
    name='ad_json',
    version=ad_json.__version__,
    packages=['ad_json'],
    url='https://github.com/youngzhiyong/ad_json',
    author=ad_json.__author__,
    author_email='youngzhiyong@yeah.net',
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='test.test_ad_json'
)
