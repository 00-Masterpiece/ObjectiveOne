def validate_time_interval(form):
    if form.start_time.data and form.end_time.data:
        if form.start_time.data >= form.end_time.data:
            raise ValidationError('Start time must be before end time.')

def darken_hex(hex_color, factor=0.8):
    """Darkens a hex color by a given factor (0–1)."""
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * factor)) for c in rgb)
    return "#{:02x}{:02x}{:02x}".format(*darkened)