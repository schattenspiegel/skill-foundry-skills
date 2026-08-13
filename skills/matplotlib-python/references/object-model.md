# Object and coordinate model

Figure owns the canvas and top-level Artists. Each Axes owns data Artists,
spines, Axis objects, labels, and legends. Transforms map data, axes, figure,
display, or blended coordinates. Keep ownership explicit: accept `Axes`, add
Artists through it, and return created objects when callers need customization.
