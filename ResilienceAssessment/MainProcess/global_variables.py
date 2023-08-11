# Define a coefficient that describes the accidental torsion
# Imagine two special moment frames are symmetrically placed at the building perimeter
# and the floor plan of the building is a regular shape (rectangle)
# If the accidental torsion is not considered -> each frame is taken 0.5 of total lateral force
# Then the ACCIDENTAL_TORSION = 1.0
# If the accidental torsion is considered -> one frame will take 0.55 of total lateral force
# since the center is assumed to be deviated from its actual location by 5% of the building dimension
# Then the ACCIDENTAL_TORSION = 0.55/0.50 = 1.1
ACCIDENTAL_TORSION = 0.55/0.50

# Define a boolean variable to determine whether the Section 12.8.6.2 is enforced or not
# Section 12.8.6.2:
# For determining the design story drifts, it is permitted to determine the elastic drifts using
# seismic design force based on the computed fundamental period without the upper limit (CuTa).
# True -> Bound by upper limit, i.e., don't impose Section 12.8.6.2
# False -> Not bound by upper limit, i.e., impose Section 12.8.6.2 requirement
# Please note this period is only for computing drift, not for computing required strength.
PERIOD_FOR_DRIFT_LIMIT = True