import unittest
import pkgutil

# from django.shortcuts import get_object_or_404

"""
NOTE:

By default CSRF validation is not applied when using APIClient.
If you need to explicitly enable CSRF validation, you can do so by
setting the enforce_csrf_checks flag when instantiating the client.

factory = APIRequestFactory(enforce_csrf_checks=True)

As usual CSRF validation will only apply to any session authenticated views.
This means CSRF validation will only occur if the client has been logged in by calling login().
"""

"""
EXAMPLES:

factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})


client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
"""

# Load all tests in this directory
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)
