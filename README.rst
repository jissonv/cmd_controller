Cmd Controller
=====
 cmd_controller is a Django app to help run the custom management commands in a more convenient way.
Some applications need to run management scripts during deployment process.
Some scripts need to run only once in a deployment and some need to run every deployment.
Run some script multiple times may corrupt the application some times.
The cmd_controller help to mark a script as re-entrant or should run only once, while during the creation of the script.
With out cmd_controller/other-app the developer need to go and remove the custom management script which should run
only once from the deployment process or from django app. The app help to achieve with out it.

Quick start
-----------

1. Add "cmd_controller" to your INSTALLED_APPS setting like this::
    INSTALLED_APPS = [
        ...
        'cmd_controller',
        ]
2. Run ``python manage.py migrate`` to create the cmd_controller models.
3. How to use it.
   Decerate the handle method with check_command and pass the script name as first parameter and Boolean value as second
   parameter. Pass True if the script can run again and again(reentrant) during deployment , False for scripts run only once.

   >> @check_command(os.path.basename(__file__).split(".")[0], <True>)  # run scripts multiple times
   >> @check_command(os.path.basename(__file__).split(".")[0], <False>) # should run only once, call agin just skips the
       execution.


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

 >> python manage.py custom_command.py  # executes the code inside the handle method only once, run the scipt again
skips the execution of the handle method.


# if the script is reentrant

class Command(BaseCommand):
    help = 'test custom command'

    @check_command(os.path.basename(__file__).split(".")[0], True)
    def handle(self, *args, **options):
        # your custom command logic

# run the script
>> python manage.py custom_command.py   # called in each deployment


