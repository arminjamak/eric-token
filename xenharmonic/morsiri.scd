/* =====================================================================================
   MORSIRI  —  a piece in a 9-note non-octave scale          (SuperCollider 3.12+)

   Period     12/5  (1515.64 c)  — an octave plus a just minor third; the scale has NO 2/1
   Generator  (96/35)^(1/5) = 349.36 c  — a tempered neutral third, chosen so that five
              generators span exactly one period plus 8/7
   MOS        LsLsLsLss   L = 231.2 c (= 8/7)   s = 118.2 c   L/s = 1.96
   Degrees    0 Vum (tonic)  1 Tol  2 Siri  3 Kun  4 Mor (pillar)  5 Ovit  6 Hilu
              7 Zish (spicy)  8 Nimo (leading tone into the next period's Vum)

   Every pitch in this file is a frequency taken from ~hz.(degree, periodShift), which
   indexes the ratio array ~ratios. Nothing is played by note name or by MIDI number.

   RUN LIVE :  evaluate the whole file (select all, Ctrl/Cmd+Enter) — it boots the server
               and plays the ~66 s piece.
   RENDER   :  MORSIRI_RENDER=out.wav sclang morsiri.scd   (offline, no audio device needed)
   ===================================================================================== */
(
// ---------------------------------------------------------------- 1. THE TUNING ----------
~tonicHz = 220.0;
~period  = 12 / 5;                              // 2.4
~gen     = ((8 / 7) * (12 / 5)) ** (1 / 5);     // 1.22364..  (349.36 c)

// nine stacked generators, folded into one period and sorted: ratios of the 9 degrees
~ratios = (0..8).collect { |k|
    var r = ~gen ** k;
    while { r >= ~period } { r = r / ~period };
    r
}.sort;
// ~ratios == [1, 1.1429 (8/7), 1.2236, 1.3984, 1.4972, 1.7111, 1.8320, 2.0937, 2.2416]

~hz = { |deg, per = 0| ~tonicHz * ~ratios[deg] * (~period ** per) };   // THE only pitch source

~cents = ~ratios.collect { |r| 1200 * log2(r) };
"Morsiri degrees (cents / Hz at tonic 220):".postln;
~ratios.do { |r, i| "  deg % : %  c   % Hz".format(i, ~cents[i].round(0.1), (~tonicHz * r).round(0.01)).postln };

// degree names used below (indices into ~ratios)
~vum = 0; ~tol = 1; ~siri = 2; ~kun = 3; ~mor = 4; ~ovit = 5; ~hilu = 6; ~zish = 7; ~nimo = 8;

// ---------------------------------------------------------------- 2. MATCHED TIMBRE ------
// Partials sit on the scale's period and its pillar (degree Mor, the tempered 3/2), iterated:
//   1, Mor, period, Mor+period, 2 periods, Mor+2 periods, 3 periods.
// Two tones a pillar or a period apart therefore share partials and do not beat. There is
// deliberately no 2/1 partial: the scale has no octave, so the instrument has none either.
~partialRatios = [
    1.0,
    ~ratios[~mor],
    ~period,
    ~ratios[~mor] * ~period,
    ~period * ~period,
    ~ratios[~mor] * ~period * ~period,
    ~period * ~period * ~period
];
~partialAmps = [1.0, 0.55, 0.50, 0.35, 0.22, 0.12, 0.06];

~pulse = 0.27;         // seconds per pulse; bars have 7 pulses grouped 3 + 2 + 2

// ---------------------------------------------------------------- 3. SCORE DATA ----------
// melody events: [degree, periodShift, pulses];  a rest is [nil, 0, pulses]
// Every two-bar phrase ends  Nimo(-1) -> Vum(0)  (or Nimo(0) -> Vum(1) in the high register):
// the small step s resolving upward into the tonic.

~intro = [                                   // 4 bars: pulse alone, then the frame chord,
    [nil, 0, 25],                            // then one cadence Nimo -> Vum as a promise
    [~nimo, -1, 1], [~vum, 0, 2]
];

~sectionA = [                                 // 8 bars, 4 phrases. Lives on Vum and Mor,
    // phrase 1: Vum up to Mor by step, back down, cadence
    [~vum, 0, 2], [~tol, 0, 1], [~siri, 0, 2], [~mor, 0, 2],
    [~kun, 0, 2], [~siri, 0, 1], [~tol, 0, 1], [~nimo, -1, 1], [~vum, 0, 2],
    // phrase 2: quicker ascent to Mor, touches Ovit (12/7), steps down, cadence
    [~vum, 0, 1], [~tol, 0, 1], [~siri, 0, 1], [~kun, 0, 2], [~mor, 0, 2],
    [~ovit, 0, 1], [~mor, 0, 1], [~kun, 0, 1], [~tol, 0, 1], [~nimo, -1, 1], [~vum, 0, 2],
    // phrase 3: starts ON the pillar, rocks Mor-Ovit-Hilu, walks down by step, cadence
    [~mor, 0, 2], [~ovit, 0, 1], [~hilu, 0, 2], [~ovit, 0, 2],
    [~mor, 0, 1], [~kun, 0, 1], [~siri, 0, 1], [~tol, 0, 1], [~nimo, -1, 1], [~vum, 0, 2],
    // phrase 4: opens with the leading-tone figure Vum-Nimo-Vum, then the phrase-1 cadence
    [~vum, 0, 1], [~nimo, -1, 1], [~vum, 0, 1], [~tol, 0, 2], [~siri, 0, 2],
    [~kun, 0, 2], [~siri, 0, 1], [~tol, 0, 1], [~nimo, -1, 1], [~vum, 0, 2]
];

~sectionB = [                                 // 8 bars. Upper half of the period: Mor, Ovit,
    // phrase 1: Mor-Ovit-Hilu, cadence up into the HIGH tonic Vum(+1)      Hilu, Nimo, Vum(+1)
    [~mor, 0, 2], [~ovit, 0, 1], [~hilu, 0, 2], [~ovit, 0, 2],
    [~hilu, 0, 2], [~ovit, 0, 1], [~hilu, 0, 1], [~nimo, 0, 1], [~vum, 1, 2],
    // phrase 2: from the high tonic down to Mor and back up, cadence
    [~vum, 1, 2], [~nimo, 0, 1], [~hilu, 0, 2], [~ovit, 0, 2],
    [~mor, 0, 2], [~ovit, 0, 1], [~hilu, 0, 1], [~nimo, 0, 1], [~vum, 1, 2],
    // phrase 3 — THE PEAK: Zish (1279 c, the spicy degree) held for three pulses over the
    // tonic frame, then resolved UP by the small step s to Nimo, and on up to Vum(+1)
    [~vum, 1, 1], [~nimo, 0, 1], [~zish, 0, 3], [~nimo, 0, 2],
    [~vum, 1, 2], [~nimo, 0, 1], [~hilu, 0, 1], [~nimo, 0, 1], [~vum, 1, 2],
    // phrase 4: descent through the whole scale back to the low tonic, cadence
    [~vum, 1, 1], [~nimo, 0, 1], [~hilu, 0, 1], [~ovit, 0, 2], [~mor, 0, 2],
    [~kun, 0, 2], [~siri, 0, 1], [~tol, 0, 1], [~nimo, -1, 1], [~vum, 0, 2]
];

// A': phrases 1-2 of A lifted one period (so they cadence Nimo(0) -> Vum(+1)), phrases 3-4 as in A
~sectionA2 = ~sectionA.copyRange(0, 19).collect { |e| [e[0], e[1] + 1, e[2]] } ++ ~sectionA.copyRange(20, 41);

~ending = [                                   // 5 bars: the cadence slowed down, then rest
    [~vum, 0, 2], [~nimo, -1, 1], [~vum, 0, 4],
    [~mor, 0, 3], [~kun, 0, 2], [~siri, 0, 2],
    [~tol, 0, 2], [~vum, 0, 1], [~nimo, -1, 2], [~vum, 0, 2],
    [~vum, 0, 7],
    [~vum, 0, 7]
];

// chords, as lists of [degree, periodShift]. Built only from the scale's three most consonant
// intervals: Mor (3/2), Nimo (9/4 = two pillars) and Kun (7/5), plus the period itself.
~chVum  = [[~vum, -1], [~mor, -1], [~vum, 0]];           // tonic frame      1 : 3/2 : 12/5
~chMor  = [[~mor, -1], [~nimo, -1], [~kun, 0]];          // on the pillar    1 : 3/2 : 9/4  (holds the leading tone Nimo)
~chHilu = [[~hilu, -1], [~tol, 0], [~ovit, 0]];          // on Hilu          1 : 3/2 : 9/4
~chSiri = [[~siri, -1], [~hilu, -1], [~tol, 0]];         // on Siri          1 : 3/2 : 9/4
~chSept = [[~vum, -1], [~kun, -1], [~vum, 0]];           // septimal colour  1 : 7/5 : 12/5
~chMorNimo = ~chMor ++ [[~nimo, 0]];                      // pillar chord with Nimo on top: catches the resolved Zish
~chFinal = [[~vum, -1], [~mor, -1], [~vum, 0], [~mor, 0], [~vum, 1]];   // the frame across two periods

// pad events: [chord, pulses];  rest is [nil, pulses].  Cadence bars are Mor 5 pulses, Vum 2.
~cad = [[~chMor, 5], [~chVum, 2]];
~padIntro = [[nil, 14], [~chVum, 7]] ++ ~cad;
~padA = [[~chVum, 7]] ++ ~cad ++ [[~chSept, 5], [~chHilu, 2]] ++ ~cad
     ++ [[~chHilu, 5], [~chSiri, 2]] ++ ~cad ++ [[~chVum, 5], [~chSiri, 2]] ++ ~cad;
~padB = [[~chHilu, 7]] ++ ~cad ++ [[~chSiri, 5], [~chHilu, 2]] ++ ~cad
     ++ [[~chVum, 5], [~chMorNimo, 2]] ++ ~cad                 // peak bar: Zish sounds over the tonic frame
     ++ [[~chHilu, 5], [~chSept, 2]] ++ ~cad;
~padA2 = ~padA.collect { |e| if(e[0].isNil) { e } { [e[0] ++ [[e[0][0][0], e[0][0][1] + 1]], e[1]] } };  // A': each chord gains its root a period up
~padEnd = [[~chMor, 3], [~chVum, 4], [~chVum, 7], [~chVum, 3], [~chMor, 2], [~chVum, 2], [~chVum, 7], [~chFinal, 7]];

~barsTotal = 33;    // 4 intro + 8 A + 8 B + 8 A' + 5 ending

// ---------------------------------------------------------------- 4. PATTERNS ------------
~melodyPat = { |events, ampl|
    Pbind(
        \instrument, \morsiri,
        \freq, Pseq(events.collect { |e| if(e[0].isNil) { Rest(1) } { ~hz.(e[0], e[1]) } }),
        \dur,  Pseq(events.collect { |e| e[2] * ~pulse }),
        \sus,  Pfunc { |ev| ev[\dur] * 0.8 },
        \atk, 0.03, \rel, 0.4, \amp, ampl, \pan, 0.15,
        \sendGate, false            // the synths free themselves; no release message needed
    )
};
~padPat = { |events, ampl|
    Pbind(
        \instrument, \morsiri,
        \freq, Pseq(events.collect { |e| if(e[0].isNil) { Rest(1) } { e[0].collect { |dp| ~hz.(dp[0], dp[1]) } } }),
        \dur,  Pseq(events.collect { |e| e[1] * ~pulse }),
        \sus,  Pfunc { |ev| ev[\dur] * 0.9 },
        \atk, 0.35, \rel, 1.4, \amp, ampl, \pan, -0.15,
        \sendGate, false
    )
};
// the pulse: 7 ticks per bar, accents on pulses 1, 4 and 6 (3 + 2 + 2). Vum one period down on
// the downbeat, Mor one period down on the other accents, a faint Vum on the weak pulses.
~tickPat = { |bars|
    Pbind(
        \instrument, \tick,
        \freq, Pseq([~hz.(~vum, -1), ~hz.(~vum, 0), ~hz.(~vum, 0), ~hz.(~mor, -1), ~hz.(~vum, 0), ~hz.(~mor, -1), ~hz.(~vum, 0)], bars),
        \amp,  Pseq([0.30, 0.06, 0.06, 0.18, 0.06, 0.18, 0.06], bars),
        \rel,  Pseq([0.22, 0.05, 0.05, 0.14, 0.05, 0.14, 0.05], bars),
        \dur, ~pulse, \pan, 0,
        \sendGate, false
    )
};

~piece = Ppar([
    ~melodyPat.(~intro ++ ~sectionA ++ ~sectionB ++ ~sectionA2 ++ ~ending, 0.28),
    ~padPat.(~padIntro ++ ~padA ++ ~padB ++ ~padA2 ++ ~padEnd, 0.11),
    ~tickPat.(~barsTotal)
]);
~lengthSec = ~barsTotal * 7 * ~pulse;
"piece length: % s of events, plus release tail".format(~lengthSec.round(0.1)).postln;

// ---------------------------------------------------------------- 5. SYNTHDEFS -----------
~defs = [
    SynthDef(\morsiri, { |out = 0, freq = 220, amp = 0.2, atk = 0.03, sus = 0.5, rel = 0.6, pan = 0|
        var env = EnvGen.kr(Env.new([0, 1, 0.8, 0], [atk, sus, rel], [3, -2, -4]), doneAction: 2);
        var sig = Mix.fill(~partialRatios.size, { |i|
            // upper partials fade faster, as in a plucked or struck body
            var fade = EnvGen.kr(Env.new([1, 1, 1 - (i * 0.1)], [atk, sus + rel]));
            SinOsc.ar(freq * ~partialRatios[i], Rand(0, 2pi)) * ~partialAmps[i] * fade
        }) / ~partialAmps.sum;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    }),
    SynthDef(\tick, { |out = 0, freq = 220, amp = 0.1, rel = 0.1, pan = 0|
        var env = EnvGen.kr(Env.perc(0.001, rel, 1, -5), doneAction: 2);
        var sig = Mix.fill(~partialRatios.size, { |i|
            SinOsc.ar(freq * ~partialRatios[i]) * ~partialAmps[i]
        }) / ~partialAmps.sum;
        Out.ar(out, Pan2.ar(sig * env * amp, pan));
    })
];

// ---------------------------------------------------------------- 6. PLAY / RENDER -------
~renderPath = "MORSIRI_RENDER".getenv;
if(~renderPath.notNil) {
    // offline render through the non-realtime server
    var score = ~piece.asScore(~lengthSec + 4);
    var freqFile = File(~renderPath ++ ".freqs.txt", "w");
    // audit trail: every frequency the score sends to the server, one per line
    score.score.do { |bundle|
        bundle.drop(1).do { |msg|
            if((msg[0] == \s_new) or: { msg[0] == 9 }) {       // 9 is the numeric code of /s_new
                var i = msg.indexOf(\freq);
                if(i.notNil) { freqFile.write(msg[i + 1].asString ++ "\n") };
            };
        };
    };
    freqFile.close;
    // the synthdefs must reach the server before the first note: put them at the head
    ~defs.reverseDo { |d| score.score = score.score.addFirst([0.0, [\d_recv, d.asBytes]]) };
    score.recordNRT(
        outputFilePath: ~renderPath, headerFormat: "WAV", sampleFormat: "int16",
        options: ServerOptions.new.numOutputBusChannels_(2).sampleRate_(44100),
        duration: ~lengthSec + 4,
        action: { "rendered to %".format(~renderPath).postln; 0.exit }
    );
} {
    s.waitForBoot {
        ~defs.do(_.add);
        s.sync;
        ~player = ~piece.play;
        "Morsiri is playing (~% s).".format((~lengthSec + 4).round).postln;
    };
};
)
