from django.db import models
from django.utils.translation import ugettext_lazy as _
from internationalflavor.countries.data import UN_RECOGNIZED_COUNTRIES, get_countries_lazy
from internationalflavor.countries.forms import CountryFormField


class CountryField(models.CharField):
    description = _('A country')

    def __init__(self, countries=UN_RECOGNIZED_COUNTRIES, exclude=(), *args, **kwargs):
        self.countries = countries
        self.exclude = exclude
        kwargs.setdefault('max_length', 2)
        self._choices = get_countries_lazy(countries, exclude)

        super(CountryField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        if self.countries != UN_RECOGNIZED_COUNTRIES:
            kwargs['countries'] = self.countries
        if self.exclude:
            kwargs['exclude'] = self.exclude
        if 'max_length' in kwargs and kwargs["max_length"] == 2:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'form_class': CountryFormField}
        defaults.update(kwargs)
        return super(CountryField, self).formfield(**defaults)