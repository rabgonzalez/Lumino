import factory
from faker import Faker

from subjects.models import Enrollment, Lesson, Subject

from .extras import RelatedFactoryVariableList
from .users import StudentFactory, TeacherFactory

fake = Faker()


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
        django_get_or_create = ('code',)

    code = factory.LazyFunction(lambda: fake.unique.bothify(text='???').upper())
    name = factory.LazyFunction(lambda: fake.sentence(nb_words=4).rstrip('.').title())
    teacher = factory.SubFactory(TeacherFactory)


class SubjectRelatedFactory(SubjectFactory):
    enrollments = RelatedFactoryVariableList(
        'factories.subjects.EnrollmentFactoryForSubject',
        factory_related_name='subject',
        size=5,
    )
    lessons = RelatedFactoryVariableList(
        'factories.subjects.LessonFactoryForSubject',
        factory_related_name='subject',
        size=5,
    )


class EnrollmentBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment
        abstract = True

    class Params:
        none_mark_probablity = 20

    student = factory.SubFactory(StudentFactory)

    @factory.lazy_attribute
    def mark(self):
        if fake.boolean(chance_of_getting_true=100 - self.none_mark_probablity):
            return fake.random_int(min=1, max=10)
        return None


class EnrollmentFactoryForSubject(EnrollmentBaseFactory):
    subject = None


class EnrollmentFactory(EnrollmentBaseFactory):
    subject = factory.SubFactory(SubjectFactory)


class LessonBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson
        abstract = True

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6).rstrip('.').title())
    content = factory.Faker('paragraph', nb_sentences=20)


class LessonFactoryForSubject(LessonBaseFactory):
    subject = None


class LessonFactory(LessonBaseFactory):
    subject = factory.SubFactory(SubjectFactory)
