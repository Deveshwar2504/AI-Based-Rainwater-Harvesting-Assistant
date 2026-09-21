def calculate_harvested_water(roof_area, rainfall, runoff_coefficient):
    """Return estimated annual harvested water as cubic metres and litres."""
    litres = roof_area * rainfall * runoff_coefficient
    volume_m3 = litres / 1000
    return volume_m3, litres


def get_recommendation(litres, roof_area):
    """Give a simple storage recommendation based on the estimated volume."""
    if litres < 10000:
        return (
            "A small storage tank or rain barrel may be suitable. "
            "Check local rainfall patterns and available space."
        )

    if litres < 50000:
        return (
            "Consider a medium-sized storage tank with a filter and overflow "
            "arrangement. Confirm that the roof and tank location are suitable."
        )

    return (
        "The estimated yield is substantial. Consider a larger storage or "
        "recharge system and seek site-specific professional guidance."
    )