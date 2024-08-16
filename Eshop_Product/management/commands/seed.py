from django_seed import Seed
from Eshop_Product.models import Product, ProductCategory, ProductTag, ProductBrand
from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def create_address():
    """Creates an address object combining different elements from the list"""

    seeder = Seed.seeder()
    seeder.add_entity(Product, 500)
    inserted_pks = seeder.execute()

    return inserted_pks


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables

    if mode == 'clear':
        return

    # Creating 15 addresses
    for i in range(1):
        create_address()