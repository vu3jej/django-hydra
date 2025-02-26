import datetime
import random
from math import ceil, floor

from django_jinja.builtins import DEFAULT_EXTENSIONS
from heroicons.jinja import heroicon_outline, heroicon_solid


# Sample code from the template
# TODO: Delete this
def random_chart(
    num_times: int = 10, num_vars: int = 2, starting_val: int = 100
) -> list[list[int]]:
    results = [[starting_val for i in range(num_vars)]]
    for _time in range(num_times - 1):
        previous_mean = sum(results[-1]) / num_vars
        results.append([])
        for var in range(num_vars):
            previous_val = (results[-2][var] + previous_mean) / 2
            results[-1].append(
                random.randrange(  # noqa
                    floor(0.5 * previous_val), ceil(2 * previous_val)  # noqa
                )  # noqa
            )
    return results


def convert_tf(item1: str | bool) -> bool:
    if item1:
        return "true"
    return ""


def prefixed_cookie(name):
    return f"{{cookiecutter.repo_name}}_{name}"


# Match all extensions but ignore admin. Use jinja2 app dirname to match builtin forms
options = {
    "match_extension": None,
    "trim_blocks": True,
    "lstrip_blocks": True,
    "app_dirname": "jinja2",
    "match_regex": r"^(?!admin/).*",
    "extensions": DEFAULT_EXTENSIONS + [
        "csp.extensions.NoncedScript",
    ],
    "context_processors": [
        "django.template.context_processors.request",
        "django.contrib.messages.context_processors.messages",
    ],
    "constants": {"csrf_cookie_name": prefixed_cookie("csrftoken")},
    "filters": {
        "template_localtime": "django.utils.timezone.template_localtime",
    },
    "globals": {
        "vite_asset": "django_vite.templatetags.django_vite.vite_asset",
        "vite_hmr_client": "django_vite.templatetags.django_vite.vite_hmr_client",
        "django_htmx_script": "django_htmx.templatetags.django_htmx.django_htmx_script",
        "heroicon_outline": heroicon_outline,
        "heroicon_solid": heroicon_solid,
        "now": datetime.datetime.utcnow,
        "template_localtime": "django.utils.timezone.template_localtime",
        "random_chart": random_chart,
        "convert_tf": convert_tf,
    },
}
