import inspect

from renardo_lib.SynthDefManagement.SCLangExperimentalPythonBindings import cls, Vibrato, RHPF
from renardo_lib.SynthDefManagement.SCLangExperimentalPythonBindings.core import instance

EnvGen = cls("EnvGen")
Env = cls("Env")


class _Effect:
    _in = "osc"

    def __init__(self):
        self.lines = []

    def __call__(self, order=0):
        def decorator(effect):
            effect_data = inspect.getargspec(effect)  # Original args and defaults

            # Get filename from function name
            filename = "{}.scd".format(effect.__name__)  # filename

            # Supplies arg names
            effect(*map(instance, effect_data.args))

            # Default values for arguments, to store
            defaults = dict(zip(effect_data.args, effect_data.defaults))

        return decorator

    def In(self):
        """ Returns 'osc', which is where In.ar() is stored """
        return self._in

    def Out(self, output):
        """ Writes to file and loads synthdef """
        print(";\n".join(self.lines))
        self.lines = []
        return output

    def add(self, *args, **kwargs):
        lines = ["{} = {}".format(key, value) for key, value in kwargs.items()]
        self.lines.extend(lines)
        return


Effect = _Effect()  # singleton


@Effect(order=0)
def vibrato(vib=0, vibdepth=0.02):
    osc = Vibrato.ar(Effect.In(), vib, depth=vibdepth)
    return Effect.Out(osc)


@Effect(order=0)
def slideTo(slide=0, sus=1, slide_delay=0):
    osc = Effect.In() * \
                    EnvGen.ar(
                        Env([1, 1, slide + 1], [sus * slide_delay, sus * (1 - slide_delay)]))
    return Effect.Out(osc)


@Effect(order=0)
def slideFrom(slide_from=0, sus=1, slide_delay=0):
    osc = Effect.In() * EnvGen.ar(Env([slide_from + 1, slide_from + 1, 1], [
                    sus * slide_delay, sus * (1 - slide_delay)]))
    return Effect.Out(osc)


# fx = FxList.new("glide", "glissando", {"glide": 0, "glide_delay": 0.5, "sus": 1}, order=0)
# fx.add("osc = osc * EnvGen.ar(Env([1, 1, (1.059463**glide)], [sus*glide_delay, sus*(1-glide_delay)]))")
# fx.save()

# fx = FxList.new("bend", "pitchBend", {"bend": 0, "sus": 1, "benddelay": 0}, order=0)
# fx.add("osc = osc * EnvGen.ar(Env([1, 1, 1 + bend, 1], [sus * benddelay, (sus*(1-benddelay)/2), (sus*(1-benddelay)/2)]))")
# fx.save()

# fx = FxList.new("coarse", "coarse", {"coarse": 0, "sus": 1}, order=0)
# fx.add("osc = osc * LFPulse.ar(coarse / sus)")
# fx.save()

# fx = FxList.new("striate", "striate", {"striate": 0, "sus": 1, "buf": 0, "rate": 1}, order=0)
# fx.add("osc = osc * LFPulse.ar(striate / sus, width:  (BufDur.kr(buf) / rate) / sus)")
# fx.save()

# fx = FxList.new("pshift", "pitchShift", {"pshift":0}, order=0)
# fx.add("osc = osc * (1.059463**pshift)")
# fx.save()


# @Effect(order=2)
# def formantFilter(formant=0):
#     Effect.add(formant=(formant % 8) + 1)
#     Effect.add(osc=Formlet.ar(Effect.In(), formant * 200, (formant %
#                5 + 1) / 1000, (formant * 1.5) / 600).tanh)
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def filterSwell(swell=0, sus=1, hpr=1):
#     env = EnvGen.kr(
#         Env([0, 1, 0], times=[(sus * 0.25), (sus * 0.25)], curve="\\sin"))
#     osc = RHPF.ar(Effect.In(), env * swell * 2000, hpr)
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def squiz(squiz=0):
#     osc = Squiz.ar(Effect.In(), pitchratio=squiz)
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def sample_atk(sample_atk=0, sample_sus=1):
#     osc = Effect.In()*EnvGen.ar(Env.new([0, 1, 0], [sample_atk, sample_sus]))
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def comp(comp=0, comp_above=1, comp_below=0.8):
#     osc = Compander.ar(osc, osc, comp, slopeBelow=comp_below,
#                        slopeAbove=comp_above, clampTime=0.01)
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def position(position=0, sus=1):
#     osc = osc * EnvGen.ar(Env([0, 0, 1], curve='step',
#                               times=[sus * position, 0]))
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def triode(triode=0):
#     osc = LeakDC.ar(osc * (osc > 0)) + (tanh(osc * (triode * 10 + 1e-3))
#                                         / (triode * 10 + 1e-3) * (osc < 0))*1.2
#     return Effect.Out(osc)
#
#
# @Effect(order=2)
# def krush(krush=0, kutoff=15000):
#     freq = Select.kr(kutoff > 0, [DC.kr(4000), kutoff])
#     signal = (osc.squared + (krush * osc)) / \
#         (osc.squared + (osc.abs * (krush-1.0)) + 1.0)
#     signal = RLPF.ar(signal, clip(freq, 20, 10000), 1)
#     osc = SelectX.ar(krush * 2.0, [osc, signal])
#     return Effect.Out(osc)
