def adjust_adjacent_regions(borders, regions, week, impact=20):
    """Adjust new infections based on adjacent regions"""
    for border in borders:
        region_name_1, region_name_2 = border
        # pylint: disable=cell-var-from-loop
        region1 = list(filter(lambda elem: elem.name == region_name_1, regions))[0]
        region2 = list(filter(lambda elem: elem.name == region_name_2, regions))[0]

        # get the new infections in current week
        region1_inf = region1.get_data_row(week).loc["New infections"]
        region2_inf = region2.get_data_row(week).loc["New infections"]

        # calculate how many new infections will be exchanged from high to low
        exchange = abs((region1_inf - region2_inf) // impact)

        # find which region has most new infections
        if region1_inf < region2_inf:
            region_high, region_low = region2, region1
        elif region1_inf > region2_inf:
            region_high, region_low = region1, region2
        else:
            continue

        # check that exchange does not exceed physical limitations
        limit_exchange = region_low.inhabitants - \
                         region_low.get_data_row(week).loc["Currently infected"] - \
                         region_low.get_data_row(week).loc["Total recoveries"] - \
                         region_low.get_data_row(week).loc["Total deaths"]

        if exchange > limit_exchange:
            exchange = limit_exchange
        print(region_high.name)
        print(region_low.name)
        print(exchange)

        # adjust the new infections
        region_high.adjust_new_infections(week, -1 * exchange)
        region_low.adjust_new_infections(week, +1 * exchange)
