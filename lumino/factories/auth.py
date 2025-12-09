import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Faker

fake = Faker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('first_name',)

    first_name = factory.LazyFunction(lambda: fake.unique.first_name())
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda obj: obj.first_name.lower())
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    profile = factory.RelatedFactory(
        'factories.users.ProfileFactory',
        factory_related_name='user',
    )

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        DEFAULT_PASSWORD = '1234'

        password = extracted or DEFAULT_PASSWORD
        self.set_password(password)
        if create:
            self.save()
