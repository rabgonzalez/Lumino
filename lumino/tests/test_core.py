import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from subjects.models import Enrollment, Lesson, Subject
from users.models import Profile

User = get_user_model()

# ==============================================================================
# Required Apps
# ==============================================================================


@pytest.mark.django_db
def test_required_apps_are_installed():
    REQUIRED_APPS = ('shared', 'accounts', 'subjects', 'users')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in REQUIRED_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(REQUIRED_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


# ==============================================================================
# Subject Model
# ==============================================================================


@pytest.mark.django_db
def test_subject_model_is_correctly_configured():
    assert (f := Subject._meta.get_field('code')), 'Subject.code no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Subject.code no tiene el tipo esperado'
    assert f.unique, 'Subject.code no se ha definido como único'

    assert (f := Subject._meta.get_field('name')), 'Subject.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Subject.name no tiene el tipo esperado'

    assert (f := Subject._meta.get_field('teacher')), 'Subject.teacher no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Subject.teacher no tiene el tipo esperado'
    assert f.related_model == User, 'Subject.teacher no referencia al modelo esperado'
    assert f.remote_field.related_name == 'teaching', (
        'Subject.teacher no tiene el related_name esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'PROTECT', (
        'Subject.teacher no tiene el método de borrado esperado'
    )

    assert (f := Subject._meta.get_field('students')), 'Subject.students no se ha definido'
    assert f.get_internal_type() == 'ManyToManyField', 'Subject.students no tiene el tipo esperado'
    assert f.related_model == User, 'Subject.students no referencia al modelo esperado'
    assert f.remote_field.related_name == 'enrolled', (
        'Subject.students no tiene el related_name esperado'
    )
    assert f.remote_field.through.__name__ == 'Enrollment', (
        'Subject.students no tiene el modelo intermedio esperado'
    )


# ==============================================================================
# Lesson Model
# ==============================================================================


@pytest.mark.django_db
def test_lesson_model_is_correctly_configured():
    assert (f := Lesson._meta.get_field('subject')), 'Lesson.subject no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Lesson.subject no tiene el tipo esperado'
    assert f.related_model == Subject, 'Lesson.subject no referencia al modelo esperado'
    assert f.remote_field.related_name == 'lessons', (
        'Lesson.subject no tiene el related_name esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Lesson.subject no tiene el método de borrado esperado'
    )

    assert (f := Lesson._meta.get_field('title')), 'Lesson.title no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Lesson.title no tiene el tipo esperado'

    assert (f := Lesson._meta.get_field('content')), 'Lesson.content no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Lesson.content no tiene el tipo esperado'
    assert f.blank, 'Lesson.content no admite valores en blanco'


# ==============================================================================
# Enrollment Model
# ==============================================================================


@pytest.mark.django_db
def test_enrollment_model_is_correctly_configured():
    assert (f := Enrollment._meta.get_field('student')), 'Enrollment.student no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Enrollment.student no tiene el tipo esperado'
    assert f.related_model == User, 'Enrollment.student no referencia al modelo esperado'
    assert f.remote_field.related_name == 'enrollments', (
        'Enrollment.student no tiene el related_name esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Enrollment.student no tiene el método de borrado esperado'
    )

    assert (f := Enrollment._meta.get_field('subject')), 'Enrollment.subject no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Enrollment.subject no tiene el tipo esperado'
    assert f.related_model == Subject, 'Enrollment.subject no referencia al modelo esperado'
    assert f.remote_field.related_name == 'enrollments', (
        'Enrollment.subject no tiene el related_name esperado'
    )
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Enrollment.subject no tiene el método de borrado esperado'
    )

    assert (f := Enrollment._meta.get_field('enrolled_at')), (
        'Enrollment.enrolled_at no se ha definido'
    )
    assert f.get_internal_type() == 'DateField', 'Enrollment.enrolled_at no tiene el tipo esperado'
    assert f.auto_now_add, 'Enrollment.enrolled_at no está configurado con auto_now_add'

    assert (f := Enrollment._meta.get_field('mark')), 'Enrollment.mark no se ha definido'
    assert f.get_internal_type() == 'PositiveSmallIntegerField', (
        'Enrollment.mark no tiene el tipo esperado'
    )
    assert f.blank, 'Enrollment.mark no admite valores en blanco'
    assert f.null, 'Enrollment.mark no admite valores nulos'
    assert f.validators[0].__class__.__name__ == 'MinValueValidator', (
        'Enrollment.mark no tiene un validador de valor mínimo'
    )
    assert f.validators[0].limit_value == 1, (
        'Enrollment.mark no tiene el valor mínimo esperado en su validador'
    )
    assert f.validators[1].__class__.__name__ == 'MaxValueValidator', (
        'Enrollment.mark no tiene un validador de valor máximo'
    )
    assert f.validators[1].limit_value == 10, (
        'Enrollment.mark no tiene el valor máximo esperado en su validador'
    )


# ==============================================================================
# Profile Model
# ==============================================================================


@pytest.mark.django_db
def test_profile_model_is_correctly_configured():
    assert (f := Profile._meta.get_field('user')), 'Profile.user no se ha definido'
    assert f.get_internal_type() == 'OneToOneField', 'Profile.user no tiene el tipo esperado'
    assert f.related_model == User, 'Profile.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Profile.user no tiene el método de borrado esperado'
    )

    assert (f := Profile._meta.get_field('role')), 'Profile.role no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Profile.role no tiene el tipo esperado'
    assert f.max_length == 1, 'Profile.role no tiene la longitud máxima esperada'
    assert f.choices == [('S', 'Student'), ('T', 'Teacher')], (
        'Profile.role no tiene las opciones esperadas'
    )

    assert (f := Profile._meta.get_field('avatar')), 'Profile.avatar no se ha definido'
    assert f.get_internal_type() in ['FileField', 'ImageField'], (
        'Profile.avatar no tiene el tipo esperado'
    )
    assert f.upload_to == 'avatars', 'Profile.avatar no tiene la ruta de subida esperada'
    assert f.default == 'avatars/noavatar.png', (
        'Profile.avatar no tiene el valor por defecto esperado'
    )
    assert f.blank, 'Profile.avatar no admite valores en blanco'

    assert (f := Profile._meta.get_field('bio')), 'Profile.bio no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Profile.bio no tiene el tipo esperado'
    assert f.blank, 'Profile.bio no admite valores en blanco'
