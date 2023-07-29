from setuptools import setup
# from distutils.core import setup
from positive_vi.version import VERSION

setup(name='positive_vi',
    version=VERSION,
    packages=[
        'positive_vi',
        'positive_vi.more',
        'positive_vi.od',
        'positive_vi.vi',
    ],
    entry_points={
        'console_scripts': [
            'pmore 	= positive_vi.more.more_main:more_main',
            'pod 	= positive_vi.od.od_main:od_main',
            'posbox = positive_vi.posbox_main:posbox_main',
            'pex 	= positive_vi.vi.ex_main:ex_main',
            'pvi 	= positive_vi.vi.vi_main:vi_main',
        ]
    }
)
