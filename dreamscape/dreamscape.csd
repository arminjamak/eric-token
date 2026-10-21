<CsoundSynthesizer>
; ---------------------------------------------------------------------------
;  "Event Horizon Lullaby" - a surrealist dreamscape backing track
;
;  Dream pop / dark pop in Eb (lydian colours, borrowed dark chords), with a
;  theremin, oscilloscope (Lissajous / scope-blip) voices, shimmer reverb and
;  sidechained pads. The bar grid is locked to the original vocal take:
;  112.2034 BPM, first downbeat at 0.2584 s.
;
;  Render:  csound dreamscape.csd   (writes an 18-channel float WAV, see Mixer)
; ---------------------------------------------------------------------------
<CsOptions>
-o dreamscape_multitrack.wav -W -f --nodisplays -m0 -d
</CsOptions>
<CsInstruments>
sr     = 48000
ksmps  = 16
nchnls = 18          ; 1-2 master, then stereo stems (see Mixer)
0dbfs  = 1

seed 1977            ; deterministic "randomness" - the dream is reproducible

giBPM  = 112.2034
giBeat = 60 / giBPM
giBar  = giBeat * 4
giOff  = 0.2584
giBars = 62
giA4   = 442         ; the vocal take sits ~+7 cents sharp of 440

gisine  ftgen 0, 0, 16384, 10, 1
githere ftgen 0, 0, 16384, 10, 1, 0.12, 0.05, 0.02     ; theremin: near-sine, faint odd/even
gisoft  ftgen 0, 0, 16384, 10, 1, 0.5, 0.33, 0.25, 0.2, 0.16, 0.14, 0.12  ; soft saw for drone

; ---------------------------------------------------------------- harmony --
; chord id -> bass note + 5-note pad voicing (pad sits above the voice)
;  0 Ebmaj9   1 F/Eb (lydian)  2 Cm9     3 Bbsus4(add9)  4 Gbmaj7
;  5 Abmaj9   6 Ebmaj7/G      7 Fm9     8 Dbmaj7#11     9 Cbmaj7#11
; 10 Bb7sus  11 Cm7          12 Fm7    13 Abm6         14 Ebm9
; 15 Emaj7#11 (neapolitan drift)
giBass[] fillarray 39, 39, 36, 34, 42, 44, 43, 41, 37, 35, 34, 36, 41, 44, 39, 40
giVoic[] fillarray 63,67,70,74,77,  63,69,72,77,79,  63,67,70,74,79,  63,65,70,72,77, \
                   61,65,70,73,78,  63,67,70,72,75,  62,67,70,75,79,  63,67,68,72,77, \
                   60,65,68,72,79,  63,66,70,75,77,  63,65,68,72,77,  63,67,70,72,79, \
                   60,63,68,72,75,  63,65,71,75,77,  61,65,66,70,73,  63,68,70,71,75

; bar -> chord. Bars 4-24 carry the vocal; their chords were chosen against
; the pitch-tracked melody (e.g. bar 15-16 hold the long Bb).
giChord[] fillarray 0,1,0,3, \
                    0,0,1,2,3,4,5,6,4,7,8,9,10, \
                    0,11,5,12,0,5,2,3, \
                    0,4,13,10,2,9,13,10,0,4,8,9,7,13,14,10, \
                    15,9,15,10,14,9,4,10,2,5,7,10, \
                    0,1,0,1,9,3,0,0,0

; section per bar: 0 intro, 1 verse A, 2 verse B, 3 voyage, 4 dissolve, 5 outro
giSect[] fillarray 0,0,0,0, 1,1,1,1,1,1,1,1,1,1,1,1,1, 2,2,2,2,2,2,2,2, \
                   3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3, 4,4,4,4,4,4,4,4,4,4,4,4, 5,5,5,5,5,5,5,5,5

giInt[]  fillarray .20,.24,.28,.32, .36,.36,.38,.40,.46,.48,.50,.50,.50,.52,.54,.58,.60, \
                   .62,.64,.64,.66,.66,.68,.70,.72, \
                   .78,.80,.80,.82,.84,.84,.86,.88,.90,.90,.92,.92,.94,.94,.96,.96, \
                   .30,.28,.26,.30,.40,.42,.44,.48,.58,.64,.70,.78, \
                   .56,.52,.50,.46,.42,.36,.28,.20,.14

; drum pattern per bar: 0 none, 1 soft pulse, 2 half-time, 3 dark-pop drive,
; 4 heartbeat, 5 snare-roll build
giDrum[] fillarray 0,0,0,0, 1,1,1,1,2,2,2,2,2,2,2,2,2, 2,2,2,2,2,2,2,2, \
                   3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3, 0,0,0,0,4,4,4,4,2,2,2,5, \
                   2,2,2,2,2,2,0,0,0

; theremin score: bar, beat, beats, midi, amp, glide(s)
giTher[] fillarray \
  1,0,3,75,.40,.60,  1,3,1,77,.42,.25,  2,0,4,82,.50,.45,  3,0,2,79,.44,.30,  3,2,2,77,.34,.30, \
  8,.5,1.5,79,.42,.30,  8,2,2,77,.42,.20,  9,0,3,82,.46,.45,  9,3,1,80,.34,.25, \
  12,.5,2,85,.34,.40,  12,2.5,1.5,82,.30,.30, \
  15,0,4,78,.24,.50,  16,0,2,80,.24,.40,  16,2,2,77,.22,.30, \
  25,1,1,70,.50,.20,  25,2,2,75,.56,.30,  26,0,2,77,.56,.25,  26,2,1,73,.52,.20,  26,3,1,70,.50,.20, \
  27,0,2,71,.54,.35,  27,2,2,75,.56,.30,  28,0,3,77,.58,.25,  28,3,1,80,.52,.20, \
  29,0,2,79,.58,.25,  29,2,2,82,.60,.30,  30,0,2,82,.60,.20,  30,2,2,78,.56,.40, \
  31,0,2,77,.56,.25,  31,2,1,75,.52,.20,  31,3,1,71,.50,.20,  32,0,2,72,.54,.25,  32,2,2,77,.58,.35, \
  33,0,1,82,.62,.25,  33,1,3,87,.66,.55,  34,0,2,85,.62,.25,  34,2,2,82,.60,.30, \
  35,0,2,84,.62,.25,  35,2,2,79,.58,.35,  36,0,4,82,.64,.30, \
  37,0,2,80,.60,.25,  37,2,2,79,.58,.20,  38,0,2,77,.58,.25,  38,2,2,75,.56,.35, \
  39,0,2,78,.58,.25,  39,2,1,77,.54,.20,  39,3,1,73,.52,.20,  40,0,2,75,.54,.25,  40,2,2,70,.40,.90, \
  41,0,4,80,.40,.80,  42,0,4,82,.42,.60,  43,0,2,83,.42,.40,  43,2,2,87,.44,.50,  44,0,4,77,.38,1.2, \
  45,0,4,78,.40,.70,  46,0,4,75,.40,.60,  47,0,2,77,.42,.40,  47,2,2,85,.44,.60,  48,0,4,84,.40,.50, \
  51,0,4,79,.26,.60,  52,0,4,77,.30,.40, \
  53,0,3,75,.46,.50,  53,3,1,77,.44,.25,  54,0,4,82,.50,.45,  55,0,2,79,.46,.30,  55,2,2,77,.44,.30, \
  56,0,4,79,.44,.40,  57,0,4,78,.42,.50,  58,0,4,77,.40,.40,  59,0,8,75,.36,.60,  61,0,4,63,.20,2.5

; ------------------------------------------------------------ busses -------
gaPadL   init 0
gaPadR   init 0
gaBasL   init 0
gaBasR   init 0
gaKeyL   init 0
gaKeyR   init 0
gaThrL   init 0
gaThrR   init 0
gaScpL   init 0
gaScpR   init 0
gaDrmL   init 0
gaDrmR   init 0
gaDrnL   init 0
gaDrnR   init 0
gaRevL   init 0
gaRevR   init 0
gaDlyL   init 0
gaDlyR   init 0
gaKick   init 0           ; sidechain key

gkThPitch init 75
gkThAmp   init 0
gkThGlide init .3
gkThAlive init 0

opcode m2f, k, k
  km xin
  xout giA4 * semitone(km - 69)
endop

opcode bartime, i, ii           ; (bar, beat) -> seconds
  ibar, ibeat xin
  xout giOff + ibar*giBar + ibeat*giBeat
endop

; ================================================================ CONDUCTOR
instr Conductor
  ibar = 0
  iarpstep = 0
  while ibar < giBars do
    ibar0    = bartime(ibar, 0)
    ich   = giChord[ibar]
    isec  = giSect[ibar]
    iint  = giInt[ibar]
    idrum = giDrum[ibar]
    iroot = giBass[ich]

    ; --- pads: one long overlapping voice per chord tone
    icut = 700 + 2600*iint
    iv = 0
    while iv < 5 do
      schedule "PadVoice", ibar0, giBar + 2.8, giVoic[ich*5+iv], 0.075 + 0.05*iint, icut, (iv+0.5)/5
      iv += 1
    od

    ; --- bass
    if idrum == 2 || idrum == 3 then
      schedule "Bass", ibar0, giBeat*1.45, iroot, 0.55
      schedule "Bass", bartime(ibar, 1.5), giBeat*0.95, iroot, 0.45
      schedule "Bass", bartime(ibar, 2.5), giBeat*1.4, iroot + (idrum == 3 && ibar % 2 == 1 ? 12 : 0), 0.45
    elseif ibar < 61 then
      schedule "Bass", ibar0, giBar*0.98, iroot, (isec == 0 || isec == 4 ? 0.3 : 0.42)
    endif

    ; --- drums
    if idrum == 1 then
      schedule "Kick", ibar0, 0.6, 0.55
      schedule "Kick", bartime(ibar, 2.5), 0.6, 0.38
      ih = 0
      while ih < 8 do
        schedule "Hat", bartime(ibar, ih*0.5 + random:i(-0.01, 0.01)), 0.12, (ih % 2 == 1 ? 0.10 : 0.05), 0
        ih += 1
      od
    elseif idrum == 2 then
      schedule "Kick", ibar0, 0.6, 0.75
      schedule "Kick", bartime(ibar, 1.5), 0.6, 0.55
      if ibar % 2 == 1 then
        schedule "Kick", bartime(ibar, 2.75), 0.6, 0.45
      endif
      schedule "Snare", bartime(ibar, 2), 1.2, 0.55 + 0.25*iint
      ih = 0
      while ih < (iint > 0.6 ? 16 : 8) do
        istep = (iint > 0.6 ? 0.25 : 0.5)
        schedule "Hat", bartime(ibar, ih*istep + random:i(-0.012, 0.012)), 0.12, (ih % 2 == 1 ? 0.12 : 0.07) * (0.7 + 0.4*iint), 0
        ih += 1
      od
      if ibar == 16 || ibar == 24 then
        schedule "Snare", bartime(ibar, 3.5), 1, 0.35
        schedule "Snare", bartime(ibar, 3.75), 1, 0.45
      endif
    elseif idrum == 3 then
      schedule "Kick", ibar0, 0.6, 0.9
      schedule "Kick", bartime(ibar, 1.5), 0.6, 0.7
      schedule "Kick", bartime(ibar, 2.5), 0.6, 0.65
      if ibar % 4 == 3 then
        schedule "Kick", bartime(ibar, 3.25), 0.6, 0.5
      endif
      schedule "Snare", bartime(ibar, 2), 1.4, 0.85
      schedule "Clap",  bartime(ibar, 2), 1.0, 0.45
      ih = 0
      while ih < 16 do
        iamp = (ih % 4 == 2 ? 0.15 : (ih % 2 == 1 ? 0.07 : 0.10))
        if ibar % 2 == 1 && ih >= 14 then
          ir = 0                        ; dark-pop hat roll (32nd triplets)
          while ir < 3 do
            schedule "Hat", bartime(ibar, ih*0.25 + ir/12), 0.08, 0.06 + 0.02*ir, 0
            ir += 1
          od
        else
          schedule "Hat", bartime(ibar, ih*0.25 + random:i(-0.008, 0.008)), 0.12, iamp, 0
        endif
        ih += 1
      od
      schedule "Hat", bartime(ibar, 3.5), 0.6, 0.08, 1  ; open hat
      if ibar == 32 || ibar == 40 then
        ir = 0
        while ir < 6 do
          schedule "Tom", bartime(ibar, 2.5 + ir*0.25), 0.8, 0.4 + 0.05*ir, 50 - ir*3
          ir += 1
        od
      endif
    elseif idrum == 4 then
      schedule "Kick", ibar0, 0.6, 0.55
      schedule "Kick", bartime(ibar, 0.5), 0.6, 0.35
    elseif idrum == 5 then
      ir = 0
      while ir < 24 do
        ipos = (ir < 8 ? ir*0.25 : 2 + (ir-8)*0.125)
        schedule "Snare", bartime(ibar, ipos), 0.5, 0.15 + 0.6*(ir/24), 1
        ir += 1
      od
      schedule "Kick", ibar0, 0.6, 0.7
      schedule "Kick", bartime(ibar, 1), 0.6, 0.7
      schedule "Kick", bartime(ibar, 2), 0.6, 0.7
      schedule "Kick", bartime(ibar, 3), 0.6, 0.7
    endif

    ; crashes on section arrivals
    if ibar == 4 || ibar == 17 || ibar == 25 || ibar == 33 || ibar == 53 then
      schedule "Crash", ibar0, 4, (ibar == 4 ? 0.16 : 0.26)
    endif
    ; reverse swells into section arrivals
    if ibar == 3 || ibar == 16 || ibar == 24 || ibar == 40 || ibar == 44 || ibar == 52 then
      schedule "RevSwell", bartime(ibar, 0), giBar, 0.22
      schedule "ScopeSweep", bartime(ibar, 0), giBar, 0.10, (ibar == 40 ? -1 : 1)
    endif

    ; --- arpeggiated star-glass motives (they shift per section)
    if isec == 0 || isec == 1 then
      ; rising/falling wave in 8ths, airy (random rests)
      iseq[] fillarray 0, 2, 4, 1, 3, 2, 4, 3
      inn = 0
      while inn < 8 do
        if random:i(0, 1) < (isec == 0 ? 0.55 : 0.8) then
          schedule "Star", bartime(ibar, inn*0.5), 1.4, giVoic[ich*5 + iseq[inn]] + 12, 0.10 + 0.05*iint, 2.0 + iint
        endif
        inn += 1
      od
    elseif isec == 2 then
      ; dotted-8th stream: one continuous line whose phase drifts against the bar
      iarpstep = (ibar == 17 ? 0 : iarpstep)
      ipos = iarpstep * 0.75 - (ibar - 17) * 4
      while ipos < 4 do
        schedule "Star", bartime(ibar, ipos), 1.6, giVoic[ich*5 + (iarpstep*3) % 5] + 12, 0.12 + 0.04*iint, 2.5
        iarpstep += 1
        ipos = iarpstep * 0.75 - (ibar - 17) * 4
      od
    elseif isec == 3 then
      ; 16ths: 3-note accent cycle over a 5-note pitch cycle, octave swaps every 2 bars
      iarpstep = (ibar == 25 ? 0 : iarpstep)
      inn = 0
      while inn < 16 do
        ipc   = (iarpstep + inn) % 5
        ioct  = (int(ibar/2) % 2 == 0 ? 12 : 24)
        iacc  = ((iarpstep + inn) % 3 == 0 ? 1 : 0.6)
        schedule "Star", bartime(ibar, inn*0.25), 0.9, giVoic[ich*5 + ipc] + ioct - (ipc > 2 ? 12 : 0), (0.08 + 0.05*iint)*iacc, 3.2
        inn += 1
      od
      iarpstep += 16
    elseif isec == 4 then
      ; triplet 8ths falling through the chord, random octave leaps; build to 16ths
      idiv = (ibar >= 49 ? 16 : 12)
      inn = 0
      while inn < idiv do
        ipc  = 4 - (inn % 5)
        ileap = (random:i(0,1) < 0.25 ? 12 : 0)
        if random:i(0, 1) < (ibar >= 49 ? 0.95 : 0.7) then
          schedule "Star", bartime(ibar, inn*4/idiv), 1.5, giVoic[ich*5 + ipc] + 12 + ileap, 0.06 + 0.06*iint, 1.8
        endif
        inn += 1
      od
    else
      ; outro: retrograde of the intro wave, thinning out
      iseq2[] fillarray 3, 4, 2, 3, 1, 4, 2, 0
      inn = 0
      while inn < 8 do
        if random:i(0, 1) < 0.85 - (ibar-53)*0.08 then
          schedule "Star", bartime(ibar, inn*0.5), 1.8, giVoic[ich*5 + iseq2[inn]] + 12, 0.10, 1.6
        endif
        inn += 1
      od
    endif

    ; --- oscilloscope blips: radar/scope pings on the 16th grid
    iprob = (isec == 3 ? 0.22 : (isec == 4 ? (ibar >= 49 ? 0.3 : 0.12) : (isec == 0 ? 0.06 : (isec == 5 ? 0.05 : 0.04))))
    inn = 0
    while inn < 16 do
      if random:i(0, 1) < iprob then
        inote = giVoic[ich*5 + int(random:i(0, 4.99))] + 24 + (random:i(0,1) < 0.3 ? 12 : 0)
        schedule "ScopeBlip", bartime(ibar, inn*0.25), 0.25, inote, 0.045 + 0.03*iint, random:i(-1, 1)
      endif
      inn += 1
    od
    ibar += 1
  od

  ; --- oscilloscope Lissajous figures: long stereo sine pairs (L=f, R=f*ratio)
  ilis[] fillarray 0,8, 9,8, 17,8, 25,8, 33,8, 41,4, 45,8, 53,8
  irat[] fillarray 1.5, 1.25, 2, 1.5, 1.3333, 1.5, 1.25, 1.5
  il = 0
  while il < 8 do
    ib = ilis[il*2]
    schedule "Lissajous", bartime(ib, 0), ilis[il*2+1]*giBar + 2, giBass[giChord[ib]] + 36, 0.05, irat[il]
    il += 1
  od

  ; --- theremin phrases
  it = 0
  while it < lenarray(giTher)/6 do
    schedule "ThNote", bartime(giTher[it*6], giTher[it*6+1]), giTher[it*6+2]*giBeat, \
             giTher[it*6+3], giTher[it*6+4], giTher[it*6+5]
    it += 1
  od
endin

; ==================================================================== VOICES
instr PadVoice
  inote = p4
  iamp  = p5
  icut  = p6
  ipan  = p7
  iatt  = 1.6
  irel  = 2.8
  aenv  linseg 0, iatt, 1, p3 - iatt - irel, 0.85, irel, 0
  kwob  randi 0.09, 0.35, 2              ; tape-wobble drift (semitones)
  klfo  lfo 0.035, 0.21 + random:i(0, 0.1)
  kcps  m2f inote + kwob + klfo
  a1    vco2 0.5, kcps * 1.0035
  a2    vco2 0.5, kcps * 0.9965
  a3    vco2 0.35, kcps * 0.5, 12        ; triangle, an octave down for body
  kcf   = icut * (1 + 0.35 * oscili:k(1, 0.07 + random:i(0, 0.05), gisine, random:i(0,1)))
  aL    moogladder2 a1 + a3*0.5, kcf, 0.18
  aR    moogladder2 a2 + a3*0.5, kcf * 1.04, 0.18
  aL    = aL * aenv * iamp
  aR    = aR * aenv * iamp
  aXL   = aL*sqrt(1-ipan)*1.2 + aR*0.25
  aXR   = aR*sqrt(ipan)*1.2 + aL*0.25
  aL    = aXL
  aR    = aXR
  gaPadL += aL
  gaPadR += aR
  gaRevL += aL * 0.55
  gaRevR += aR * 0.55
endin

instr Bass
  inote = p4
  iamp  = p5
  aenv  linseg 0, 0.012, 1, p3 - 0.1, 0.8, 0.088, 0
  kcps  m2f inote
  a1    poscil 1, kcps
  a2    vco2 0.25, kcps, 12
  asig     = tanh((a1 + a2) * 1.6) * 0.7
  asig     butterlp asig, 380
  asig     = asig * aenv * iamp
  gaBasL += asig
  gaBasR += asig
endin

instr Kick
  iamp  = p4
  kf    expseg 140, 0.04, 58, 0.25, 42, p3, 40
  aenv  expseg 1, 0.02, 0.8, p3 - 0.02, 0.001
  a1    poscil aenv, kf
  aclk  rand 1
  aclk  butterhp aclk * expseg(1, 0.006, 0.001, 1, 0.001), 3000
  asig     = tanh((a1 + aclk*0.25) * 1.4) * iamp
  gaKick += asig
  gaDrmL += asig
  gaDrmR += asig
  gaRevL += asig * 0.04
  gaRevR += asig * 0.04
endin

instr Snare
  iamp  = p4
  isoft = p5                            ; 1 = roll / ghost
  anz   rand 1
  anz   butterbp anz, 2400, 2600
  anv   expseg 1, 0.15 + (isoft == 1 ? 0 : 0.08), 0.001
  atn   poscil expseg:k(1, 0.09, 0.001), expseg:k(230, 0.05, 180)
  asig     = (anz * anv * 0.9 + atn * 0.6) * iamp
  asig     butterhp asig, 140
  gaDrmL += asig * 0.95
  gaDrmR += asig
  gaRevL += asig * (isoft == 1 ? 0.2 : 0.6)
  gaRevR += asig * (isoft == 1 ? 0.2 : 0.6)
  gaDlyL += asig * 0.08
endin

instr Clap
  iamp  = p4
  anz   rand 1
  anz   butterbp anz, 1300, 1400
  aenv  linseg 0, 0.001, 1, 0.01, 0.2, 0.001, 1, 0.01, 0.2, 0.001, 1, 0.12, 0
  asig     = anz * aenv * iamp
  gaDrmL += asig * 0.8
  gaDrmR += asig
  gaRevL += asig * 0.5
  gaRevR += asig * 0.5
endin

instr Hat
  iamp  = p4
  iopen = p5
  anz   rand 1
  anz   butterhp anz, 7500
  anz   butterhp anz, 7500
  aenv  expseg 1, (iopen == 1 ? 0.35 : 0.045), 0.001
  asig     = anz * aenv * iamp
  ipan  random 0.35, 0.65
  gaDrmL += asig * sqrt(1-ipan)
  gaDrmR += asig * sqrt(ipan)
  gaRevL += asig * 0.15
  gaRevR += asig * 0.15
endin

instr Tom
  iamp  = p4
  kcps  expseg cpsmidinn(p5 + 12), 0.08, cpsmidinn(p5), p3, cpsmidinn(p5)
  asig     poscil expseg(1, p3, 0.001), kcps
  asig     = tanh(asig * 1.3) * iamp
  gaDrmL += asig * 0.8
  gaDrmR += asig
  gaRevL += asig * 0.4
  gaRevR += asig * 0.4
endin

instr Crash
  iamp  = p4
  anz   rand 1
  anz   butterhp anz, 4500
  aenv  expseg 1, p3, 0.001
  aL    = anz * aenv * iamp
  aR    delay aL, 0.011
  gaDrmL += aL
  gaDrmR += aR
  gaRevL += aL * 0.5
  gaRevR += aR * 0.5
endin

instr RevSwell                          ; reverse-cymbal swell into a downbeat
  iamp  = p4
  anz   rand 1
  kcf   expseg 800, p3, 9000
  anz   butterbp anz, kcf, kcf * 0.6
  aenv  expseg 0.001, p3 * 0.97, 1, p3 * 0.03, 0.001
  asig     = anz * aenv * iamp
  gaDrmL += asig
  gaDrmR += asig
  gaRevL += asig * 0.6
  gaRevR += asig * 0.6
endin

instr Star                              ; glassy FM "starlight" bell for the arps
  inote = p4
  iamp  = p5
  indx  = p6
  icps  = giA4 * semitone(inote - 69)
  kidx  expseg indx, p3, 0.05
  aenv  expseg 0.001, 0.004, 1, p3 - 0.004, 0.001
  asig     foscili aenv * iamp, icps, 1, 3.5, kidx, gisine
  a2    poscil aenv * iamp * 0.4, icps * 2.003
  asig     = asig + a2
  ipan  random 0.15, 0.85
  aL    = asig * sqrt(1-ipan)
  aR    = asig * sqrt(ipan)
  gaKeyL += aL
  gaKeyR += aR
  gaRevL += aL * 0.5
  gaRevR += aR * 0.5
  gaDlyL += (aL + aR) * 0.35
endin

; ------------------------------------------------------------- THEREMIN ---
instr ThNote                            ; sets the theremin's target while held
  gkThPitch = p4
  gkThAmp   = p5
  gkThGlide = p6
  gkThAlive = 1
endin

instr Theremin                          ; one continuous voice: glides, vibrato, swells
  kalive = gkThAlive
  gkThAlive = 0
  ktarg  = (kalive == 1 ? gkThAmp : 0)
  kamp   portk ktarg, (kalive == 1 ? 0.09 : 0.35)
  kp     portk gkThPitch, gkThGlide * 0.45
  ; delayed vibrato: deepens the longer the hand holds still
  kstill = (abs(kp - gkThPitch) < 0.05 ? 1 : 0)
  kvd    portk kstill * 0.22, 0.8
  kvib   oscili kvd, 5.6 + randi:k(0.4, 1.3)
  kcps   m2f kp + kvib + randi:k(0.03, 4)
  asig      oscili 1, kcps, githere
  asig      butterlp asig, 3200
  asig      = asig * kamp * 0.55
  aL     delay asig, 0.0007
  gaThrL += aL
  gaThrR += asig
  gaRevL += aL * 0.16
  gaRevR += asig * 0.16
  gaDlyL += asig * 0.1
endin

; ---------------------------------------------------------- OSCILLOSCOPE ---
instr Lissajous                         ; L = sin(f), R = sin(f*ratio + drift) -> rotating figure
  inote = p4
  iamp  = p5
  irat  = p6
  icps  = giA4 * semitone(inote - 69)
  aenv  linseg 0, p3*0.3, 1, p3*0.4, 1, p3*0.3, 0
  kdr   = 0.17 + randi:k(0.08, 0.2)        ; slow detune makes the figure turn
  kcrt  randh 0.004, 9                     ; stepped "phosphor" jitter
  aL    poscil aenv * iamp, icps * (1 + kcrt)
  aR    poscil aenv * iamp, icps * irat + kdr
  aR2   poscil aenv * iamp * 0.3, icps * irat * 2 + kdr*2
  gaScpL += aL
  gaScpR += aR + aR2
  gaRevL += aL * 0.35
  gaRevR += (aR + aR2) * 0.35
endin

instr ScopeBlip                         ; trace "ping": sine pip with pitch flick + ring mod
  inote = p4
  iamp  = p5
  ipan  = (p6 + 1) / 2
  icps  = giA4 * semitone(inote - 69)
  idir  random -1, 1
  kf    expseg icps * (idir > 0 ? 0.5 : 2), 0.025, icps, p3, icps
  aenv  expseg 0.001, 0.002, 1, 0.06, 0.15, p3 - 0.062, 0.001
  asig     poscil aenv * iamp, kf
  arm   poscil 1, icps * 1.414
  asig     = asig * (0.75 + 0.25*arm)
  gaScpL += asig * sqrt(1-ipan)
  gaScpR += asig * sqrt(ipan)
  gaDlyL += asig * 0.5
  gaRevL += asig * 0.3
  gaRevR += asig * 0.3
endin

instr ScopeSweep                        ; time-base sweep riser / faller
  iamp  = p4
  idir  = p5
  kf    expseg (idir > 0 ? 120 : 4000), p3, (idir > 0 ? 4000 : 90)
  aenv  linseg 0, p3*0.8, 1, p3*0.2, 0
  a1    poscil 1, kf
  a2    poscil 1, kf * 1.5 + 3
  aL    = a1 * aenv * iamp
  aR    = a2 * aenv * iamp
  gaScpL += aL
  gaScpR += aR
  gaRevL += aL * 0.5
  gaRevR += aR * 0.5
endin

; ---------------------------------------------------------------- DRONE ---
instr Drone                             ; Eb pedal + solar-wind noise, gated by the form
  ktime timeinsts
  kbar  = limit(int((ktime - giOff) / giBar), 0, giBars - 1)
  ksec  = giSect[kbar]
  kg    portk (ksec == 4 && kbar < 45 ? 0.1 : (ksec == 0 ? 0.7 : 1)), 3
  kg    = kg * linseg(0, 6, 1, p3 - 12, 1, 6, 0)
  a1    oscili 0.25, giA4 * semitone(39 - 69 - 12) * (1 + randi:k(0.002, 0.3)), gisoft
  a2    oscili 0.18, giA4 * semitone(46 - 69 - 12) * 1.002, gisoft
  a3    oscili 0.12, giA4 * semitone(39 - 69), gisoft
  kcf   = 260 + 180 * oscili:k(1, 0.031)
  ad    moogladder2 a1 + a2 + a3, kcf, 0.35
  anz   pinkish 1
  kbp   = 900 * pow(4, oscili:k(1, 0.019))
  aw    butterbp anz, kbp, kbp * 0.3
  aw    = aw * (0.05 + 0.04 * oscili:k(1, 0.11))
  aL    = (ad * 0.8 + aw) * kg
  aR    = (ad * 0.8 + delay(aw, 0.013)) * kg
  gaDrnL += aL
  gaDrnR += aR
  gaRevL += aL * 0.4
  gaRevR += aR * 0.4
endin

; ================================================================== MIXER
; out channels: 1-2 master | 3-4 pads | 5-6 bass | 7-8 star keys | 9-10 theremin
;               11-12 oscilloscope | 13-14 drums | 15-16 drone | 17-18 fx returns
instr Mixer
  ktime timeinsts
  kbar  = limit(int((ktime - giOff) / giBar), 0, giBars - 1)
  kint  = giInt[kbar]

  ; sidechain: kick ducks pads/bass/drone, deeper in the dark-pop sections
  aKenv follow2 gaKick, 0.002, 0.2
  kdep  portk (kint > 0.75 ? 0.5 : 0.25), 1
  kduck = 1 - kdep * limit(k(aKenv) * 2.5, 0, 1)
  kduck portk kduck, 0.004

  aPL = gaPadL * kduck * 3.2
  aPR = gaPadR * kduck * 3.2
  aBL = gaBasL * (0.5 + 0.5*kduck) * 0.6
  aBR = gaBasR * (0.5 + 0.5*kduck) * 0.6
  aKL = gaKeyL * 1.7
  aKR = gaKeyR * 1.7
  aTL = gaThrL * 0.32
  aTR = gaThrR * 0.32
  aSL = gaScpL * 1.4
  aSR = gaScpR * 1.4
  aDL = gaDrmL * 0.55
  aDR = gaDrmR * 0.55
  aNL = gaDrnL * kduck * 0.7
  aNR = gaDrnR * kduck * 0.7

  ; ping-pong dotted-8th delay, darkened feedback
  aFb   init 0
  adl   delayr 2
  atapL deltap giBeat * 0.75
        delayw gaDlyL + gaDlyR + aFb * 0.48
  adr   delayr 2
  atapR deltap giBeat * 0.75
        delayw atapL
  aFb   butterlp atapR, 3500
  aFb   butterhp aFb, 250
  aEL   = atapL * 0.5
  aER   = atapR * 0.5
  gaRevL += aEL * 0.4
  gaRevR += aER * 0.4

  ; shimmer reverb: reverb tail pitched up an octave and fed back in
  aShL  init 0
  aShR  init 0
  aWL, aWR reverbsc gaRevL + aShL * 0.22, gaRevR + aShR * 0.22, 0.91, 8500
  fsL   pvsanal aWL, 2048, 512, 2048, 1
  fsR   pvsanal aWR, 2048, 512, 2048, 1
  fuL   pvscale fsL, 2
  fuR   pvscale fsR, 2
  aShL  pvsynth fuL
  aShR  pvsynth fuR
  aShL  butterhp aShL, 700
  aShR  butterhp aShR, 700
  aWL   butterhp aWL, 120
  aWR   butterhp aWR, 120
  aFxL  = aWL * 0.55 + aEL
  aFxR  = aWR * 0.55 + aER

  aML = aPL + aBL + aKL + aTL + aSL + aDL + aNL + aFxL
  aMR = aPR + aBR + aKR + aTR + aSR + aDR + aNR + aFxR
  ; soft ceiling (glue compression happens in mix.py, without look-ahead delay)
  aML = tanh(aML * 0.6) / 0.6 * 0.5
  aMR = tanh(aMR * 0.6) / 0.6 * 0.5

  outc aML, aMR, aPL, aPR, aBL, aBR, aKL, aKR, aTL, aTR, aSL, aSR, aDL, aDR, aNL, aNR, aFxL, aFxR

  clear gaPadL, gaPadR, gaBasL, gaBasR, gaKeyL, gaKeyR, gaThrL, gaThrR, gaScpL, gaScpR
  clear gaDrmL, gaDrmR, gaDrnL, gaDrnR, gaRevL, gaRevR, gaDlyL, gaDlyR, gaKick
endin

</CsInstruments>
<CsScore>
i "Conductor" 0 0.01
i "Theremin"  0 140
i "Drone"     0 140
i "Mixer"     0 140
e
</CsScore>
</CsoundSynthesizer>
