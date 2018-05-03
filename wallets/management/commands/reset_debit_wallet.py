from distutils.util import strtobool

from django.core.management.base import BaseCommand

from wallets.models import Wallet


class Command(BaseCommand):
    help = 'Reset debit wallet to zero'

    def add_arguments(self, parser):
        pass

    def prompt(self, query):
        self.stdout.write('%s [y/n]: ' % query)
        val = raw_input()
        try:
            ret = strtobool(val)
        except ValueError:
            self.stdout.write('Please answer with a y/n\n')
            return self.prompt(query)
        return ret

    def print_waiting_dot(self):
        self.stdout.write("..", ending='')
        self.stdout.flush()

    def handle(self, *args, **options):

        if self.prompt("You are about to reset debit wallet balance, are you sure?"):

            debit_wallet = Wallet.objects.filter(type__id='debit').first()
            debit_wallet.balance = 0
            debit_wallet.save()

            self.stdout.write("Balance reset to zero")
