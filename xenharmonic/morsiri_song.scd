/* =====================================================================================
   WHERE THE SLOW MOON GOES  —  instrumental tracks of the Morsiri song  (SuperCollider 3.12+)

   Reads song.json (written by song.py: the single source of truth for tuning, groove, chords,
   bass, arpeggio and melody) and either plays it live or renders it offline.

   Every pitch is a frequency copied from song.json, where it was produced by the tuning array
   (220 Hz * ratios[degree] * (12/5)^k). No note names, no MIDI numbers anywhere.

   RUN LIVE :  evaluate the whole file.
   RENDER   :  MORSIRI_RENDER=song_instrumental.wav sclang morsiri_song.scd
   GUIDE    :  MORSIRI_GUIDE=1 adds the vocal melody as a synth lead (instrumental-only listening)
   ===================================================================================== */
(
var path = thisProcess.nowExecutingPath;
var dir = if(path.notNil) { path.dirname } { File.getcwd };
var song = File.readAllString(dir +/+ "song.json").parseJSON;   // parseJSON delivers numbers as Strings
var pulse = song["pulse"].asFloat;
var period = song["period"].asFloat;
var ratios = song["ratios"].collect(_.asFloat);
var morRatio = ratios[4];                                      // the pillar degree
var totalSec = song["bars"].asInteger * 7 * pulse;
// matched spectrum, identical to morsiri.scd: period and pillar, iterated
var partials = [1.0, morRatio, period, morRatio * period, period * period, morRatio * period * period, period * period * period];
var pamps = [1.0, 0.55, 0.50, 0.35, 0.22, 0.12, 0.06];
var defs, synthFor, panFor, list, score, renderPath, guide;

"% — % bars, % s".format(song["title"], song["bars"], totalSec.round(0.1)).postln;

defs = [
    // sustained chord pad: the matched spectrum with a slow swell
    SynthDef(\pad, { |out = 0, freq = 220, amp = 0.1, sus = 1, pan = 0|
        var env = EnvGen.kr(Env.new([0, 1, 0.8, 0], [0.25, sus * 0.9, 1.2], [2, -2, -4]), doneAction: 2);
        var sig = Mix.fill(partials.size, { |i|
            SinOsc.ar(freq * partials[i], Rand(0, 2pi)) * pamps[i]
            * EnvGen.kr(Env.new([1, 1, 1 - (i * 0.1)], [0.25, sus + 1.2]))
        }) / pamps.sum;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    }),
    // plucked arpeggio: same partials, upper ones die quickly
    SynthDef(\pluck, { |out = 0, freq = 440, amp = 0.1, sus = 0.15, pan = 0|
        var len = (sus * 2.2).max(0.25);
        var env = EnvGen.kr(Env.perc(0.004, len, 1, -5), doneAction: 2);
        var sig = Mix.fill(partials.size, { |i|
            SinOsc.ar(freq * partials[i], Rand(0, 2pi)) * pamps[i] * EnvGen.kr(Env.perc(0.001, len / (1 + (i * 0.8)), 1, -4))
        }) / pamps.sum;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    }),
    // bass: fundamental, pillar and period partials only, low-passed
    SynthDef(\bass, { |out = 0, freq = 90, amp = 0.2, sus = 0.3, pan = 0|
        var env = EnvGen.kr(Env.linen(0.012, sus * 0.85, 0.14, 1, -2), doneAction: 2);
        var sig = SinOsc.ar(freq) + (SinOsc.ar(freq * morRatio) * 0.35) + (SinOsc.ar(freq * period) * 0.18);
        sig = LPF.ar(sig, 650) + (SinOsc.ar(freq) * 0.25);
        Out.ar(out, Pan2.ar(sig * env * amp / 1.6, pan));
    }),
    // kick: a thump that falls from one period above its pitch down to it (tuned to 12/5, not to an octave)
    SynthDef(\kick, { |out = 0, freq = 91.7, amp = 0.5, sus = 0.3, pan = 0|
        var penv = EnvGen.kr(Env.new([period, 1], [0.045], -4));
        var env = EnvGen.kr(Env.perc(0.002, 0.3, 1, -6), doneAction: 2);
        var click = HPF.ar(WhiteNoise.ar(0.25), 3000) * EnvGen.kr(Env.perc(0.001, 0.012));
        Out.ar(out, Pan2.ar((SinOsc.ar(freq * penv) + click) * env * amp, pan));
    }),
    // clap: unpitched band-limited noise burst with a tiny flam
    SynthDef(\clap, { |out = 0, freq = 0, amp = 0.2, sus = 0.2, pan = 0|
        var env = EnvGen.kr(Env.new([0, 1, 0.3, 1, 0], [0.001, 0.018, 0.004, 0.13], [0, -3, 0, -5]), doneAction: 2);
        var sig = BPF.ar(WhiteNoise.ar, 1900, 0.8) * 2;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    }),
    // hat: unpitched high noise tick
    SynthDef(\hat, { |out = 0, freq = 0, amp = 0.1, sus = 0.1, pan = 0|
        var env = EnvGen.kr(Env.perc(0.001, 0.045, 1, -4), doneAction: 2);
        Out.ar(out, Pan2.ar(HPF.ar(WhiteNoise.ar, 8000) * env * amp, pan));
    }),
    // guide lead (only with MORSIRI_GUIDE): the sung melody on the matched timbre
    SynthDef(\lead, { |out = 0, freq = 220, amp = 0.2, sus = 0.5, pan = 0|
        var env = EnvGen.kr(Env.new([0, 1, 0.8, 0], [0.03, sus * 0.85, 0.3], [3, -2, -4]), doneAction: 2);
        var sig = Mix.fill(partials.size, { |i| SinOsc.ar(freq * partials[i], Rand(0, 2pi)) * pamps[i] }) / pamps.sum;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    })
];
synthFor = (pad: \pad, pluck: \pluck, bass: \bass, kick: \kick, clap: \clap, hat: \hat, vocal: \lead);
panFor = (pad: -0.2, pluck: 0.3, bass: 0, kick: 0, clap: 0.15, hat: -0.3, vocal: 0.05);
guide = "MORSIRI_GUIDE".getenv.notNil;

// one flat, time-sorted list of server messages built from song.json
list = List.new;
song["events"].keysValuesDo { |name, evs|
    var synth = synthFor[name.asSymbol];
    if(synth.notNil and: { (name != "vocal") or: guide }) {
        evs.do { |ev|
            var t = ev["t"].asFloat * pulse, d = ev["d"].asFloat * pulse, a = ev["a"].asFloat;
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
    score.add([totalSec + 5, [\c_set, 0, 0]]);
    defs.reverseDo { |d| score.score = score.score.addFirst([0.0, [\d_recv, d.asBytes]]) };   // defs before any note
    score.recordNRT(
        outputFilePath: renderPath, headerFormat: "WAV", sampleFormat: "int16",
        options: ServerOptions.new.numOutputBusChannels_(2).sampleRate_(44100),
        duration: totalSec + 5,
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
