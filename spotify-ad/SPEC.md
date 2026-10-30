# Spotify spec ad — "One app. Every song."

GOAL:    the viewer feels Spotify is the one place their listening lives, and remembers the mark.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Reference: a neon-thread spec ad (person's upload).
TIME:    25 s x 30 = 750 frames. No music source in this session (no HeyGen, model hosts blocked):
         sound is effects only, every effect on a visible action.
LOOK:    ground #040806 with a 0.35 radial green lift (#0B2416) behind the hero, no texture.
         ink #EFFFF5, quiet ink #7F9A8A. Accent: Spotify green #1ED760, only on the thread,
         the mark, one word or number per shot. The tagline shot inverts: green ground, #04140A ink.
         Display: Inter Display Black 900, 88–200 px, tracking -3%. Body: Inter SemiBold 600, 30–44 px.
         Medium: one neon thread (core #DFFFE9 4 px + green 12 px, glow drop-shadows 8 px @0.9 and
         26 px @0.55) that travels the whole film and draws the objects it reaches.
OBJECTS: the Spotify mark (simple-icons path, brand file, never redrawn); a phone (420 x 860,
         64 px radius, near-black glass #0B120E, 3 px edge) playing a track with lyrics;
         playlist covers (380 px squares, flat two-colour art with the playlist name);
         a Wrapped minute counter; a Jam queue card with four friends; five devices.
MOTION:  enter expo.out / power4.out; camera and floods power2.inOut; exits and zoom-throughs
         power3.in; pops back.out(1.6). Moves 0.3–0.6 s. Word stagger 0.067 s. Exits 40–50% of entrances.
SHOTS:   f0–90     intro: thread spirals in, burst, mark springs in, name wipes beside it; thread leaves right.
         f90–210   phone: thread enters left and traces the phone; track plays, lyrics light in turn,
                   "100M+ songs" left; zoom through the album art.
         f210–306  discover: the album art shrinks back into the front cover; covers fan out;
                   "Discover Weekly"; whip left.
         f306–402  wrapped: arrives from the right; bars rise; minutes count to 48,213; chips pop; blur swap.
         f402–492  jam: four friends thread into one queue; each arrival adds a song; whip up.
         f492–576  devices: thread branches from below to five devices that light up; green flood.
         f576–642  tagline on green: "One app." / "Every song."; the green irises down to the mark's circle.
         f642–750  end: the circle is the mark; name wipes in; "Listen free at spotify.com";
                   spec-ad note and "made by fanad"; hold 2 s.
BANNED:  floating particles, purple/blue gradients, glass cards, three cards in a row, KPI grids,
         everything fading and sliding up, titles that drift after landing, logo docked in a corner,
         corner labels and HUD decoration, synthesised tones.
QA:      f45 burst, f80 lockup, f150 phone + lyrics, f205 zoom-through, f240 covers, f370 counter landed,
         f460 jam queue full, f550 devices lit, f620 tagline, f730 end card readable.
