import random

def rng(sides):
    """
    Roll a dice with the given number of sides.
    """
    return random.randint(1, sides)

def random_weather(type: str = None, region: str = None):
    """
    Generates a random weather condition.
    If `type` is None, generates completely random weather.
    If `region` is specified, generates weather specific to that region.
    """
    # Weather categories and conditions
    weather_conditions = {
        "general": ["sunny", "partly cloudy", "overcast", "rainy", "stormy", "foggy"],
        "hot": ["scorching heat", "hot and dry", "humid and sunny", "blistering winds"],
        "cold": ["freezing", "snowy", "icy winds", "light snow", "frosty"],
        "wet": ["light rain", "heavy rain", "drizzle", "thunderstorm", "downpour"],
        "dry": ["arid", "clear skies", "hot and dry", "cool and dry"],
        "windy": ["breezy", "gusty winds", "strong gales", "howling winds", "calm"],
    }

    # Region-specific conditions
    region_conditions = {
        "mountain": ["cold and windy", "foggy", "snowfall", "thunderstorm", "clear skies"],
        "desert": ["scorching heat", "arid", "hot winds", "dust storm", "clear skies"],
        "swamp": ["humid and misty", "drizzling rain", "foggy", "heavy rain", "overcast"],
        "forest": ["light rain", "sunny", "overcast", "breezy", "stormy"],
        "plains": ["sunny", "breezy", "partly cloudy", "rainy", "clear skies"],
        "coast": ["humid and windy", "stormy", "sunny", "overcast", "drizzle"],
    }

    # Determine weather based on the inputs
    if region and region in region_conditions:
        weather = random.choice(region_conditions[region])
    elif type and type in weather_conditions:
        weather = random.choice(weather_conditions[type])
    elif not type and not region:
        # Completely random weather
        category = random.choice(list(weather_conditions.keys()))
        weather = random.choice(weather_conditions[category])
    else:
        # Handle invalid type or region
        weather = "Invalid weather type or region provided."

    return weather
