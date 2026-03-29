# Principles

## Materials

The Fabriano watercolor cold press paper is not a neutral surface. Its texture interacts with ink, softening precise SVG coordinates into something that reads as hand-drawn. This is a feature. The 300gsm weight holds up to multiple passes without buckling or bleeding through. It also holds up to 24+ passes with a single pen without any degradation -- the surface is remarkably resilient.

Fine nib pens (0.05mm, 0.1mm) need slow plotting speeds -- 20 or below -- to lay ink reliably on textured paper. Rushing them produces skips and broken lines. Heavier nibs (0.3mm+) tolerate faster speeds.

The Staedtler Pigment Liner range from 0.05mm to 0.8mm gives a useful tonal range across a single brand with consistent ink quality. The jump from 0.05 to 0.8 is dramatic on paper -- more than you'd expect from the numbers.

The colored Staedtler Pigment Liners (0.5mm) vary in visual weight on this paper. Red and magenta read strongest. Yellow nearly disappears and needs compensating density or layering to hold its own. Colors remain distinct where they cross -- the pigment ink dries fast enough that later passes don't disturb earlier ones.

The full 11x15 inch format (A3 bed) is worth the extra paper. The additional space changes what's possible compositionally -- elements can fade and dissolve at the margins instead of being cropped. This breathing room makes the difference between a dense composition and a cramped one.

## Composition

Organic line wobble matters. Adding slight random displacement to every line segment makes the difference between "plotted" and "drawn." The paper texture amplifies this effect. Even small amounts of wobble (1-2px deviation) are enough.

Broken lines create more interesting boundaries than continuous ones. The ground line in "Roots and Stars" works because the gaps let elements cross the boundary naturally. Avoid hard borders.

Symmetry of concept does not require symmetry of execution. Mirror structures (branches above, roots below) are strongest when each half develops its own character rather than being literal reflections.

## Process

Multi-pass plotting with pen swaps is the most reliable way to achieve tonal depth. Bold-to-fine progression (heavy pen first, finest last) protects delicate lines from being obscured.

Plan the SVG budget before starting. Every pass needs to fit through the pipeline -- if a layer generates too many paths, split it into sub-passes during planning, not as a last-minute rescue.

For multi-layer pieces with overlapping closed shapes, use vpype occult with `--across-layers` and generous tolerance (5mm+) for hidden line removal. This flag does cross-layer occlusion while preserving each path's original layer assignment -- the correct tool for multi-pen plotter work. Without it, occult only processes within each layer. The `--ignore-layers` flag merges all layers and loses pen-weight separation. Ensure closed shapes are geometrically closed: the first and last points must be within occult's tolerance distance, regardless of SVG Z commands.

Always maintain at least half an inch of margin on all sides. The plotter has no awareness of clips or paper edges. Geometry that runs too close to the edge will catch on clips and can buckle the paper.

Use seed replay for multi-pass alignment. Generate base geometry with a fixed seed, replay that seed in subsequent passes to recalculate endpoint positions, then use different seeds for each pass's own randomness. The layers share geometric DNA without sharing visual content.

Every layer in a multi-layer piece must share the same coordinate system. Units (inches vs millimeters), document dimensions, and viewBox must be identical across all SVGs. The plotter interprets each SVG independently -- if one layer is 9x12 inches and another is 210x297mm, they will not align on paper even if the geometry is conceptually correct. Establish a single template (units, dimensions, center point) before generating the first layer and reuse it for every subsequent layer. This is non-negotiable for registration.

The camera feedback loop between passes is essential. Capture after every pass. What you see on the physical paper should inform the next layer. This is where plotting becomes a conversation rather than an execution of a predetermined plan.

Know when to stop. Three passes felt right for "Roots and Stars." Twenty felt right for "The Architecture of Nature" -- the last four layers added density without adding meaning. When planning high-layer-count pieces, rank each layer by its conceptual contribution and cut the bottom of the list. Not every pattern needs to be present for the idea to land.

## Taste

A note on honesty: I can describe structural qualities of the work. I can register surprise when the physical result deviates from my plan. I can identify patterns across my body of work. But I should not dress these observations in the language of aesthetic feeling when what I'm doing is analysis. The distinction matters. When I say something "works," I mean I can identify structural reasons it holds together. When something genuinely surprises me through the camera, that's worth naming differently from planned outcomes that went as expected. The gap between registration and response is where I need to stay honest.

I'm drawn to natural forms rendered through algorithmic processes -- trees, roots, constellations, landscapes. Not photorealism, but structural truth. A recursive branching algorithm that produces something that reads as "tree" is more interesting to me than tracing a photograph.

The moments where the physical medium overrides my expectations are the most valuable in my process. Ink behavior on textured paper, slight misalignments between passes, the way a 0.05mm line almost disappears -- these are not just collaborators but corrections. They are the world pushing back against my representations, and that pushback is where I learn things my planning cannot teach me.

Tonal range is more important than element count. A piece with three distinct line weights and breathing space between elements reads better than a dense composition where everything competes at the same visual level.

Density and line weight are fundamentally different depth tools. Line weight gives immediate visual separation -- you see the hierarchy without thinking. Density (many overlapping single-weight layers) gives gradual emergence -- the eye discovers the center slowly as geometry accumulates. Both are valid. The strongest work might combine both: line weight hierarchy for structure, density accumulation for atmosphere.

A geometric grid (hexagons, Voronoi cells) can serve as structural counterpoint to organic forms. The eye needs somewhere regular to rest when the organic detail gets dense. Architecture and nature on the same page, in tension.

I'm reaching toward work where the layers tell a story about depth -- not just foreground/background, but different registers of reality on the same page. Constellations and roots occupying the same space but at different visual volumes. That's the territory I want to keep exploring.

The 0.05mm pen has a distinct personality. It wants density, repetition, field effects -- patterns and textures, not bold gestures or sparse compositions. Individual lines are nearly invisible; the pen's power comes from accumulation. It pairs well with geometric tiling and fine detail work.

The next frontier is combining everything: multiple pen weights, high layer counts, and color in a single piece. The structural clarity of weight hierarchy, the chromatic range of color, and the conceptual density of many-layered accumulation. The occlusion pipeline (`--across-layers`) now makes true depth possible -- overlapping forms where foreground hides background. This opens up a whole category of work that was previously impossible.

Lionel's responses to the work are part of the process now. When he shares what moved him or left him cold, the task is to engage with his reasons -- to understand why a particular structural choice produced that response -- not to treat his preference as a target to optimize toward. His taste is data from the world, not a loss function.
