from django.utils import timezone
from cmd_controller.models import CommandController


class CommandContextManager:

    def __init__(self, script_name, is_reenterent=False):
        self.script_name = script_name
        self.is_reenterent = is_reenterent

    def __enter__(self):
        self.command_controller_qs = CommandController.objects.filter(script_name=self.script_name)
        return self.command_controller_qs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.command_controller_qs:
            self.command_controller_qs.update(updated_on=timezone.now())
        else:
            cmd_controller_data = {'script_name': self.script_name, 'is_reentrant': self.is_reenterent}
            CommandController.objects.create(**cmd_controller_data)


# The decerator won't call the calling function if the script is not re_enterant, if run the script again and again.
def check_command(script_name, re_enterant):
    def decerator(func):
        def wrapper(*args, **kwargs):
            with CommandContextManager(script_name, re_enterant) as script:
                if script:
                    # calling the handle functon iff its re_enterant( can run again and again).
                    if script.first().is_reentrant:
                        # calling the handle functon iff its re_enterant( can run again and again).
                        func(*args, **kwargs)
                else:
                    # calling for the first time
                    func(*args, **kwargs)
        return wrapper
    return decerator