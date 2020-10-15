def adjust_adjacent_regions(borders, regions, week, impact=20):
    """Adjust new infections based on adjacent regions"""
    for border in borders:
        region_name_1, region_name_2 = border
        region1 = list(filter(lambda elem: elem.name == region_name_1, regions))[0]
        region2 = list(filter(lambda elem: elem.name == region_name_2, regions))[0]

        region1_inf = region1.get_new_infections(week)
        region2_inf = region2.get_new_infections(week)

        exchange = abs((region1_inf - region2_inf) // impact)

        if region1_inf < region2_inf:
            region_high = region2
            region_low = region1
        elif region1_inf > region2_inf:
            region_high = region1
            region_low = region2
        region_high.adjust_new_infections(week, -1 * exchange)
        region_low.adjust_new_infections(week, +1 * exchange)