from setuptools import setup
# from distutils.core import setup
from positive_box.version import VERSION

setup(name='positive_box',
    version=VERSION,
    packages=[
        'positive_box',
        'positive_box.editors',
        'positive_box.od',
        'positive_box.searching',
        'positive_box.sorting',
    ],
    entry_points={
        'console_scripts': [
            'ped 	= positive_box.searching.ed_main:ed_main',
            'pex 	= positive_box.editors.ex_main:ex_main',
            'pgrep 	= positive_box.searching.grep_main:grep_main',
            'pmore 	= positive_box.editors.more_main:more_main',
            'pod 	= positive_box.od.od_main:od_main',
            'posbox = positive_box.posbox_main:posbox_main',
            'psed 	= positive_box.searching.sed_main:sed_main',
            'psort 	= positive_box.sorting.sort_main:sort_main',
            'ptsort = positive_box.sorting.tsort_main:tsort_main',
            'pvi 	= positive_box.editors.vi_main:vi_main',
        ]
    }
)
