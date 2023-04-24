from django.core.management.base import BaseCommand
import os
import subprocess

class Command(BaseCommand):
    help = 'Builds the Sphinx documentation.'

    def handle(self, *args, **options):
        docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', '..', '..', '..', 'docs'))
        try:
            subprocess.run(['make', 'html'], cwd=docs_dir, check=True)
        except subprocess.CalledProcessError as err:
            self.stderr.write(self.style.ERROR(
                f"The documentation build failed "
                f"with exit code {err.returncode}"))
