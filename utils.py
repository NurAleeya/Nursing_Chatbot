def calc_fluid_requirement(weight_kg: float) -> str:
    """
    Calculates daily maintenance fluid requirement using the Holliday-Segar formula.
    
    - 100 ml/kg for first 10 kg
    - 50 ml/kg for next 10 kg
    - 20 ml/kg for every kg above 20 kg
    """
    if weight_kg <= 0:
        return "Invalid weight."
    
    if weight_kg <= 10:
        total = weight_kg * 100
    elif weight_kg <= 20:
        total = 1000 + (weight_kg - 10) * 50
    else:
        total = 1500 + (weight_kg - 20) * 20

    return f"Estimated Daily Fluid Requirement: {total:.0f} ml/day"
