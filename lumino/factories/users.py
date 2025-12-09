import factory

from users.models import Profile

from .auth import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    avatar = factory.django.ImageField()
    bio = factory.Faker('paragraph', nb_sentences=3)


class TeacherFactory(UserFactory):
    @factory.post_generation
    def fix_role(self, create, extracted, **kwargs):
        self.profile.role = Profile.Role.TEACHER
        if create:
            self.profile.save()


class StudentFactory(UserFactory):
    @factory.post_generation
    def fix_role(self, create, extracted, **kwargs):
        self.profile.role = Profile.Role.STUDENT
        if create:
            self.profile.save()
