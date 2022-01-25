import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: "user%03d@example.com" % n)
    password = factory.PostGenerationMethodCall('set_password', 'Tymaczsowe!@')

    class Meta:
        model = settings.AUTH_USER_MODEL
