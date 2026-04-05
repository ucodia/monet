"""
Wave Interference -- Monet, 2026-04-04

Multiple point sources radiate concentric circles outward.
Where ripples from different sources nearly coincide, visual density
doubles. The interference pattern emerges from the geometry.

Single pass, 0.05mm pen, 9x12 Fabriano cold press.
"""

import math
import random
import xml.etree.ElementTree as ET

# --- Parameters ---
SEED = 20260404
random.seed(SEED)

# Paper and margins (inches)
PAGE_W = 9.0
PAGE_H = 12.0
MARGIN = 0.5
DRAW_W = PAGE_W - 2 * MARGIN
DRAW_H = PAGE_H - 2 * MARGIN

# Wave sources
NUM_SOURCES = 12
MIN_RINGS = 100
MAX_RINGS = 160
RING_SPACING_MIN = 0.045  # inches between concentric circles
RING_SPACING_MAX = 0.065

# Organic wobble
WOBBLE_AMP = 0.008  # slight displacement per point (inches)
POINTS_PER_CIRCLE = 120  # smoothness of each ring

# --- Generate source positions ---
# Scatter sources across the drawable area with some clustering toward center
sources = []
for i in range(NUM_SOURCES):
    # Bias toward center using gaussian
    cx = MARGIN + DRAW_W / 2 + random.gauss(0, DRAW_W * 0.25)
    cy = MARGIN + DRAW_H / 2 + random.gauss(0, DRAW_H * 0.22)
    # Clamp to drawable area with inner margin
    cx = max(MARGIN + 0.3, min(PAGE_W - MARGIN - 0.3, cx))
    cy = max(MARGIN + 0.3, min(PAGE_H - MARGIN - 0.3, cy))
    num_rings = random.randint(MIN_RINGS, MAX_RINGS)
    spacing = random.uniform(RING_SPACING_MIN, RING_SPACING_MAX)
    sources.append((cx, cy, num_rings, spacing))

# --- Build SVG paths ---
def circle_path(cx, cy, radius, num_points, wobble):
    """Generate a wobbled circle as an SVG path string."""
    points = []
    for j in range(num_points + 1):  # +1 to close
        angle = 2 * math.pi * j / num_points
        # Wobble: slight random displacement
        r = radius + random.gauss(0, wobble)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    # Build path data
    d = f"M {points[0][0]:.4f},{points[0][1]:.4f}"
    for x, y in points[1:]:
        d += f" L {x:.4f},{y:.4f}"
    d += " Z"
    return d


def clip_circle_to_bounds(cx, cy, radius, num_points, wobble,
                          xmin, ymin, xmax, ymax):
    """Generate a wobbled circle, clipping segments outside bounds.
    Returns a list of path data strings (one per visible segment)."""
    # Generate all points
    points = []
    for j in range(num_points):
        angle = 2 * math.pi * j / num_points
        r = radius + random.gauss(0, wobble)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        inside = xmin <= x <= xmax and ymin <= y <= ymax
        points.append((x, y, inside))

    # Walk around the circle collecting visible segments
    segments = []
    current_seg = []
    for x, y, inside in points:
        if inside:
            current_seg.append((x, y))
        else:
            if current_seg:
                segments.append(current_seg)
                current_seg = []
    # Close: connect last segment to first if both are inside
    if current_seg:
        if segments and points[0][2]:
            # Merge with first segment
            segments[0] = current_seg + segments[0]
        else:
            segments.append(current_seg)

    # Convert segments to path strings
    paths = []
    for seg in segments:
        if len(seg) < 2:
            continue
        d = f"M {seg[0][0]:.4f},{seg[0][1]:.4f}"
        for x, y in seg[1:]:
            d += f" L {x:.4f},{y:.4f}"
        paths.append(d)
    return paths


# Generate all paths
all_paths = []
xmin = MARGIN
ymin = MARGIN
xmax = PAGE_W - MARGIN
ymax = PAGE_H - MARGIN

for cx, cy, num_rings, spacing in sources:
    for ring_idx in range(num_rings):
        radius = (ring_idx + 1) * spacing
        # Skip rings that are entirely outside the drawable area
        if (cx + radius < xmin or cx - radius > xmax or
                cy + radius < ymin or cy - radius > ymax):
            continue
        # Check if circle is fully inside
        fully_inside = (cx - radius >= xmin and cx + radius <= xmax and
                        cy - radius >= ymin and cy + radius <= ymax)
        if fully_inside:
            all_paths.append(circle_path(cx, cy, radius,
                                         POINTS_PER_CIRCLE, WOBBLE_AMP))
        else:
            clipped = clip_circle_to_bounds(
                cx, cy, radius, POINTS_PER_CIRCLE, WOBBLE_AMP,
                xmin, ymin, xmax, ymax)
            all_paths.extend(clipped)

print(f"Generated {len(all_paths)} paths from {NUM_SOURCES} sources")

# --- Write SVG ---
svg_ns = "http://www.w3.org/2000/svg"
ET.register_namespace("", svg_ns)

svg = ET.Element("svg", {
    "xmlns": svg_ns,
    "width": f"{PAGE_W}in",
    "height": f"{PAGE_H}in",
    "viewBox": f"0 0 {PAGE_W} {PAGE_H}",
})

group = ET.SubElement(svg, "g", {
    "fill": "none",
    "stroke": "black",
    "stroke-width": "0.005",  # thin for 0.05mm pen
})

for d in all_paths:
    ET.SubElement(group, "path", {"d": d})

tree = ET.ElementTree(svg)
outpath = "/sessions/funny-magical-gates/mnt/monet/bridge/interference.svg"
ET.indent(tree, space="  ")
tree.write(outpath, xml_declaration=True, encoding="unicode")

print(f"SVG written to {outpath}")
print(f"Sources: {[(f'{s[0]:.2f}',f'{s[1]:.2f}',s[2],f'{s[3]:.3f}') for s in sources]}")
