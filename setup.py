from setuptools import setup, find_packages


setup(
    name='xxsite',
    version='${version}',
    description='内容发布工具',
    author='firerick',
    author_email='rickdonma@gmail.com',
    url='',
    license='MIT',
    packages=find_packages('xxsite'),
    package_dir={'': 'xxsite'},
    include_package_data = True,
    install_requires=[
        'django~=2.2',
        'gunicorn==20.0.0',
        'supervisor==4.1.0',
        'mysqlclient==1.4.4',
        'django-redis==4.9.0',
        'mistune==0.8.4',
        'hiredis==0.2.0',
        'redis==2.10.6',
        # debug
        'django-debug-toolbar==1.9.1',
        'Pympler==0.5',
    ],
    scripts=[
        'xxsite/manage.py',
        'xxsite/xxsite/wsgi.py',
    ],
    entry_points={
        'console_scripts': [
            'xxsite_manage = manage:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
)
