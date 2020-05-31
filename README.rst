Cmd Controller
=====
 cmd_controller is a Django app to help run the custom management command in a more convenient way,
Most of the time during deployment, develpers need to run some django management scripts,
some script need to run only once and some need to run again and again.
Running some scripts again and again may corrupt the application. The cmd_controller help to mark a script reentrant,
while during the creation of the script and skips the scripts which are not reentrant.


Quick start
-----------

1. Add "cmd_controller" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cmd_controller',
    ]

2. Run ``python manage.py migrate`` to create the cmd_controller models.

3. How to use it.
   import cmd_utils import check_command in your custom django command, and decerate the handle
   method and pass the script name as first parameter and Boolean value as second parameter. Pass True if the
   script can run again and again(reentrant), False for scripts run only once.

   >> @check_command(os.path.basename(__file__).split(".")[0], <True>)  # need to run scripts multiple times
   >> @check_command(os.path.basename(__file__).split(".")[0], <False>) # should run only once.


app/management/commands/<custom_command.py>
# if the script should run only once.

import os
from django.core.management.base import BaseCommand
from cmd_controller.cmd_utils import check_command


class Command(BaseCommand):
    help = 'test custom command'

    @check_command(os.path.basename(__file__).split(".")[0], False)
    def handle(self, *args, **options):
        # your custom command logic


# if the script is reentrant

class Command(BaseCommand):
    help = 'test custom command'

    @check_command(os.path.basename(__file__).split(".")[0], True)
    def handle(self, *args, **options):
        # your custom command logic

# run the script
>> python manage.py custom_command.py



