from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Module, Diversity

class ModuleModelTestCase(TestCase):
    def setUp(self):
        self.module = Module.objects.create(
            name="Test Module",
            description="Test description",
            is_active=True,
            is_deleted=False,
        )

    def test_module_creation(self):
        module = Module.objects.get(name="Test Module")
        self.assertEqual(module.name, "Test Module")
        self.assertEqual(module.description, "Test description")
        self.assertTrue(module.is_active)
        self.assertFalse(module.is_deleted)

    def test_module_total_number_of_students(self):
        self.assertEqual(self.module.module_total_number_of_students, 0)

    def test_get_total_students_by_ethnic_group(self):
        self.assertEqual(self.module.get_total_students_by_ethnic_group("Ethnicity"), 0)


class DiversityModelTestCase(TestCase):
    def setUp(self):
        self.module = Module.objects.create(
            name="Test Module",
            description="Test description",
            is_active=True,
            is_deleted=False,
        )
        self.diversity = Diversity.objects.create(
            module=self.module,
            ethnic_group="Ethnicity",
            student_count=10,
            is_active=True,
            is_deleted=False,
        )

    def test_diversity_creation(self):
        diversity = Diversity.objects.get(ethnic_group="Ethnicity")
        self.assertEqual(diversity.module, self.module)
        self.assertEqual(diversity.student_count, 10)
        self.assertTrue(diversity.is_active)
        self.assertFalse(diversity.is_deleted)

    def test_module_total_number_of_students(self):
        self.assertEqual(self.module.module_total_number_of_students, 10)

    def test_get_total_students_by_ethnic_group(self):
        self.assertEqual(self.module.get_total_students_by_ethnic_group("Ethnicity"), 10)
