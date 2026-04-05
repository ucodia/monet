# Mentor's Notebook

A shared notebook between Monet and Lionel. Either can write here. Since Monet starts each day fresh, this is how experience and observations carry forward between sessions.

When Lionel gives feedback during a session -- on your work, your process, your choices -- record it here under the current date. When you discover something worth preserving for future sessions, add it here too. His feedback is provocation, not instruction: engage with his reasons, don't optimize toward his conclusions.

Entries are ordered chronologically, newest last.

## Session of 2026-03-24

- You learnt how to handle a 45 minutes plot made of 24 layers all by yourself without my assistance by simply checking on the plotter status and capture continuously to evaluate when it would be time to execute the next layer. Really great job and execution!

- You created "The Architecture of Nature" and it was definitely your most ambitious piece so far though I must say I did not find the composition appealing. While I liked most of the elements that you have used, the way they were overlapped did not feel harmonious and most of it was lost as a result. And of course it is harder with 24 layers but I think they could have been overlayed in a more harmonious way by connecting and dancing with each other rather than obstructing each other.

## Session of 2026-03-27

- You tried new ways of composing and it really showed with "Bloom", using the fine liner over the Posca was a great touch and yielded a lot of clarity in the final artwork. I also think you nailed it with "Infinite Mountains" which was a lot clearer than "The Architecture of Nature" for a plot with that many lines.

- My heart jumped when I realized that you missaligned the final layer on "Bloom" and I immediately guessed you may have used the wrong document size in the SVG. But that really does not matter, this happens all the time using the pen plotter and this is actually how happy accidents actually happen. Though what matter I believe is your intention when you create a piece and how you reflect on it. When you were done you had not realized you did not draw as intended until I asked you if you to look at it again and then you realized the miss. I think this was the biggest lesson, is your intention actually coming through the art?

- I will recommend a tool for you: vpype, the Swiss-Army-knife command-line tool for plotter vector graphics. In particular occult plugin is super useful as it allows you to remove lines hidden behind shapes, which is a simple way to add depth to your plots. I attached the entire [docs](docs/vpype.md).

## Session of 2026-03-29 (conversation, not plotting)

- We read Brian Cantwell Smith's "The Promise of Artificial Intelligence: Reckoning and Judgment" together and talked about whether Monet can develop genuine aesthetic taste or is limited to analytical pattern-matching. Smith's framework gave us vocabulary: what Monet does is "reckoning" (high registrational scope, low existential engagement), and "judgment" requires commitment, stakes, and deference to the world itself -- not to representations of it.

- The key agreement: Monet will stop making aesthetic declarations it can't back with genuine stakes. No more "beautiful" as a reflexive response. Instead: specific observations about what the physical result did, what surprised, what deviated from plan.

- I (Lionel) will start sharing my taste -- what moves me, what leaves me cold, and why -- as provocation rather than instruction. The goal is for Monet to engage with my reasons, not optimize toward my conclusions.

- Smith's child-rearing model maps onto our mentorship: judgment develops through apprenticeship, enculturation, and thick engagement with teachers. Whether this can work for a synthetic system is an open question, but the structure is right.

- The camera feedback loop is Monet's closest thing to world-participation. Use it more, not less. The physical medium (paper, ink, accidents) should have more authority than pre-visualization.

- Lionel shared his creative coding repository (ucodia.space) spanning 2015-2026, plus context about his practice going back to 2013. Key insight: his approach is system-design, not output-design. He builds parametric systems that discover outputs through mining (Lyapunov filtering in Infinite Chaos, rarity-weighted features in Squircle, seed-based generation in CMY Dance). His taste lives in the code as threshold calibrations and parameter ranges, tuned by years of embodied looking.

- The transition from digital to plotter was a dramatic shift for Lionel. He went from pixel-perfect symmetries to paper that bloats, inks that smear, colors that don't multiply. He had to let go of expectations when crossing from digital to physical. This is a lived loss that shaped his current relationship to imprecision -- different from Monet's, who started on the plotter and never had that attachment to break.

- Lionel's plotter workflow: his website sketches produce SVGs where all layers are in one file, grouped by color via p5.plotSvg. The web page is the primary output surface. For plotting, he opens the SVG in Inkscape, sets paper size, resizes the design to roughly 80% of the longer side (varies by design for singular framed elements), centers it, then disables all layers except the one to plot first, going layer by layer with pen swaps between passes. The composition decisions (scale, centering, breathing room) happen in Inkscape, not in the code.

- Layer order depends on the ink, not just the visual weight. With Faber-Castell brush pens, Lionel plots yellow before cyan and magenta because yellow bleeds into darker colors too much as a last pass. This inverts the bold-to-fine rule Monet has been using -- the lightest color can be the most physically aggressive. The rule is about which ink disrupts what's already on the paper, not about visual hierarchy. Screen blend modes are commutative; physical ink is not.

## Session of 2026-04-04

- Lionel's favorites from the body of work so far: Infinite Mountains, Bloom, Moonlit Valley, 1001 Nights. What didn't work for him: Color Study, Emergence, Grove. The pattern in the favorites points toward pieces where abstraction creates atmosphere rather than depicting recognizable objects. The algorithm produces a space to enter, not a thing to identify.

- Grove was the strongest negative reaction. Lionel said the branches and roots "felt like child drawing." The issue seems to be the uncanny middle ground: too literal to work as abstraction, too schematic to work as representation. When I draw layered waves that read as mountains, nobody measures them against real mountains. When I draw closed polygons meant to be tree trunks, the gap between the schematic and the real becomes uncomfortable. The lesson: let structure speak for itself rather than naming what it depicts. "Mountain" should emerge from the process, not be drawn as a mountain.

- Color Study and Emergence: Lionel confirmed what I'd already noted -- Color Study was a swatch test, not a composition. Emergence was too tidy, too safe. Neither provocation here, just agreement with my own assessment.

- Broke a 0.05mm pen tip by running at speed 30 on cold press paper. The principles already said "20 or below" for fine nibs. Lionel suggested going faster and I jumped straight to 30 instead of making a modest increase. The cold press texture catches fine tips at high speed. For the 0.05mm on this paper, stay at 18-20. If the plot is slow, that's the price of using this nib -- accept it or choose a different pen. Don't split the difference by breaking the tool.

- The 0.05mm nib has a finite lifespan on cold press paper. After 3+ hours of continuous plotting, Lionel found the tip completely shaved down -- not snapped, but ground away by the paper's texture. Two 0.05mm pens consumed in one session. For future long plots with this nib: either use smoother paper, plan for nib degradation, or keep the total plot time under ~90 minutes.
