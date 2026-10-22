import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda n: 'user-{n}'.format(n=n))
    first_name = factory.Sequence(lambda n: 'User {n}'.format(n=n))
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'user-{n}@claritydev.net'.format(n=n))

    class Meta:
        model = User


class SuperUserFactory(UserFactory):

    is_staff = True
    is_superuser = True
