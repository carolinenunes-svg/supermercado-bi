
import os, sys, traceback
from streamlit.testing.v1 import AppTest

try:
    print('Testing dashboard via Streamlit AppTest...')
    at = AppTest.from_file('dashboard.py', default_timeout=30)
    at.run()
    if at.exception:
        print('EXCEPTION in AppTest:')
        for exc in at.exception:
            print(exc)
        sys.exit(1)
    print('AppTest executed cleanly!')
    print('Tabs count:', len(at.tabs))
    print('Sidebar widgets:', len(at.sidebar))
    print('SUCCESS')
except Exception as e:
    print('AppTest error:', e)
    traceback.print_exc()
