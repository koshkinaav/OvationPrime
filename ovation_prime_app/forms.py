from django.forms import Form, DateTimeField, ChoiceField, DecimalField


class OvationPrimeConductanceForm(Form):
    dt = DateTimeField(required=True)
    _type = ChoiceField(choices=[('pedgrid', 'pedgrid'), ('hallgrid', 'hallgrid')], required=True)


class WeightedFluxForm(Form):
    dt = DecimalField(required=True)
    atype = ChoiceField(choices=[('diff', 'diff'), ('mono', 'mono'), ('wave', 'wave'), ('ions', 'ions')],
                        initial='diff', required=False)


season_choices = [
    ('winter', 'winter'),
    ('spring', 'spring'),
    ('summer', 'summer'),
    ('fall', 'fall'),
]


class SeasonalFluxForm(Form):
    dt = DateTimeField(required=True)
    atype = ChoiceField(choices=[('diff', 'diff'), ('mono', 'mono'), ('wave', 'wave'), ('ions', 'ions')],
                        initial='diff', required=False)
    jtype = ChoiceField(choices=[('energy', 'energy'), ('number', 'number')], initial='energy', required=False)

    seasonN = ChoiceField(choices=season_choices, initial='summer', required=False)
    seasonS = ChoiceField(choices=season_choices, initial='winter', required=False)

    dF = DecimalField(required=False, initial=2134.17)

