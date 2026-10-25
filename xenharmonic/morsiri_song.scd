/* =====================================================================================
   WHERE THE SLOW MOON GOES  —  the band  (SuperCollider 3.12+)
   A slow swing ballad in the Morsiri scale (period 12/5): piano comping, upright bass in two,
   brushes, a clarinet-like lead. Reads song.json written by song.py (the single score source).
   Every pitch is a frequency copied from song.json, produced there by the tuning array; no
   note names, no MIDI numbers anywhere. The instruments use the matched spectrum of the scale
   (partials on the period and the pillar), so the band is in tune with the non-octave tuning.

   RUN LIVE :  evaluate the whole file.
   RENDER   :  MORSIRI_RENDER=song_instrumental.wav sclang morsiri_song.scd
   GUIDE    :  MORSIRI_GUIDE=1 adds the sung melody on the lead instrument
   ===================================================================================== */
(
var path = thisProcess.nowExecutingPath;
var dir = if(path.notNil) { path.dirname } { File.getcwd };
var song = File.readAllString(dir +/+ "song.json").parseJSON;   // numbers arrive as Strings
var unit = song["pulse"].asFloat;
var period = song["period"].asFloat;
var ratios = song["ratios"].collect(_.asFloat);
var morRatio = ratios[4];
var totalSec = song["bars"].asInteger * song["units_per_bar"].asInteger * unit;
var partials = [1.0, morRatio, period, morRatio * period, period * period, morRatio * period * period, period * period * period];
var pamps = [1.0, 0.55, 0.50, 0.35, 0.22, 0.12, 0.06];
var defs, synthFor, panFor, list, score, renderPath, guide;

"% — % bars, % s".format(song["title"], song["bars"], totalSec.round(0.1)).postln;

defs = [
    // piano: struck matched-spectrum tone, upper partials die first, a touch of hammer noise
    SynthDef(\piano, { |out = 0, freq = 220, amp = 0.1, sus = 1, pan = 0|
        var len = (sus * 1.6).clip(0.5, 3.5);
        var env = EnvGen.kr(Env.perc(0.003, len, 1, -4), doneAction: 2);
        var sig = Mix.fill(partials.size, { |i|
            SinOsc.ar(freq * partials[i], Rand(0, 2pi)) * pamps[i] * EnvGen.kr(Env.perc(0.001, len / (1 + (i * 0.9)), 1, -3))
        }) / pamps.sum;
        var hammer = LPF.ar(WhiteNoise.ar(0.08), 2500) * EnvGen.kr(Env.perc(0.0005, 0.012));
        Out.ar(out, Pan2.ar((sig + hammer) * env * amp, pan));
    }),
    // piano left hand: same tone, darker, longer
    SynthDef(\pianobass, { |out = 0, freq = 90, amp = 0.15, sus = 1, pan = 0|
        var len = (sus * 1.4).clip(0.6, 2.5);
        var env = EnvGen.kr(Env.perc(0.004, len, 1, -4), doneAction: 2);
        var sig = (SinOsc.ar(freq) + (SinOsc.ar(freq * morRatio) * 0.35) + (SinOsc.ar(freq * period) * 0.3)
            + (SinOsc.ar(freq * morRatio * period) * 0.12)) / 1.8;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    }),
    // upright bass: plucked, round, with a finger thump
    SynthDef(\bass, { |out = 0, freq = 90, amp = 0.3, sus = 0.5, pan = 0|
        var len = (sus * 1.1).clip(0.3, 2.0);
        var env = EnvGen.kr(Env.new([0, 1, 0.45, 0], [0.008, len * 0.4, len * 0.6], [-2, -3, -4]), doneAction: 2);
        var sig = SinOsc.ar(freq) + (SinOsc.ar(freq * morRatio) * 0.28) + (SinOsc.ar(freq * period) * 0.14);
        var thump = LPF.ar(BrownNoise.ar(0.5), 350) * EnvGen.kr(Env.perc(0.002, 0.05));
        sig = LPF.ar(sig, 1100) * 0.7;
        Out.ar(out, Pan2.ar((sig + thump) * env * amp, pan));
    }),
    // brushes on a snare: a slow swish of filtered noise
    SynthDef(\brush, { |out = 0, freq = 0, amp = 0.3, sus = 0.8, pan = 0|
        var env = EnvGen.kr(Env.new([0, 1, 0], [0.11, (sus * 0.5).clip(0.2, 1.2)], [2, -3]), doneAction: 2);
        var sig = BPF.ar(WhiteNoise.ar, 3200, 1.2) + (HPF.ar(WhiteNoise.ar, 6000) * 0.4);
        Out.ar(out, Pan2.ar(sig * env * amp * 0.5, pan));
    }),
    // ride tick: short, high
    SynthDef(\ride, { |out = 0, freq = 0, amp = 0.1, sus = 0.1, pan = 0|
        var env = EnvGen.kr(Env.perc(0.001, 0.14, 1, -5), doneAction: 2);
        var sig = HPF.ar(WhiteNoise.ar, 7000) + (SinOsc.ar(5100 + Rand(-200, 200)) * 0.15);
        Out.ar(out, Pan2.ar(sig * env * amp * 0.6, pan));
    }),
    // clarinet-like lead: the matched spectrum with breath, slow attack and a singer's vibrato
    SynthDef(\lead, { |out = 0, freq = 220, amp = 0.2, sus = 0.5, pan = 0|
        var vib = 1 + (SinOsc.kr(4.9, Rand(0, 2pi)) * 0.004 * EnvGen.kr(Env.new([0, 0, 1], [0.25, 0.3])));
        var env = EnvGen.kr(Env.new([0, 1, 0.85, 0], [0.09, (sus * 0.92).max(0.05), 0.22], [2, -2, -4]), doneAction: 2);
        var sig = Mix.fill(partials.size, { |i| SinOsc.ar(freq * partials[i] * vib, Rand(0, 2pi)) * pamps[i] }) / pamps.sum;
        var breath = BPF.ar(WhiteNoise.ar(0.05), freq * 4, 0.5);
        Out.ar(out, Pan2.ar((sig + breath) * env * amp, pan));
    })
];
synthFor = (piano: \piano, pianobass: \pianobass, bass: \bass, brush: \brush, ride: \ride, lead: \lead, vocal: \lead);
panFor = (piano: 0.25, pianobass: 0.2, bass: -0.1, brush: -0.35, ride: -0.3, lead: 0.35, vocal: 0.0);
guide = "MORSIRI_GUIDE".getenv.notNil;

list = List.new;
song["events"].keysValuesDo { |name, evs|
    var synth = synthFor[name.asSymbol];
    if(synth.notNil and: { (name != "vocal") or: guide }) {
        evs.do { |ev|
            var t = ev["t"].asFloat * unit, d = ev["d"].asFloat * unit, a = ev["a"].asFloat;
            if(name == "vocal") { a = 0.16 };
            ev["f"].do { |fs|
                list.add([t, [\s_new, synth, -1, 0, 0, \freq, fs.asFloat, \amp, a, \sus, d, \pan, panFor[name.asSymbol]]]);
            };
        };
    };
};
list = list.asArray.sort { |x, y| x[0] <= y[0] };
"% server messages".format(list.size).postln;

renderPath = "MORSIRI_RENDER".getenv;
if(renderPath.notNil) {
    score = Score.new(list);
    score.add([totalSec + 6, [\c_set, 0, 0]]);
    defs.reverseDo { |d| score.score = score.score.addFirst([0.0, [\d_recv, d.asBytes]]) };
    score.recordNRT(
        outputFilePath: renderPath, headerFormat: "WAV", sampleFormat: "int16",
        options: ServerOptions.new.numOutputBusChannels_(2).sampleRate_(44100),
        duration: totalSec + 6,
        action: { "rendered to %".format(renderPath).postln; 0.exit }
    );
} {
    s.waitForBoot {
        defs.do(_.add);
        s.sync;
        Routine {
            var now = 0;
            list.do { |item|
                var t = item[0], msg = item[1];
                (t - now).wait; now = t;
                Synth(msg[1], msg.copyRange(5, msg.size - 1));
            };
        }.play(SystemClock);
        "playing % (% s)".format(song["title"], totalSec.round).postln;
    };
};
)
