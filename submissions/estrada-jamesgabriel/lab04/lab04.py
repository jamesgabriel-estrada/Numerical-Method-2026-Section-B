# PART 1: Geometric Series
def geometric_sum(x, N):
    """Calculate the partial sum of a geometric series up to N terms."""
    total = 0.0
    for k in range(N + 1):
        total += x ** k
    return total

# Testing Part 1
x_values = [0.5, 0.8, 0.9]
N_terms = 15

for x in x_values:
    approx = geometric_sum(x, N_terms)
    exact = 1 / (1 - x)
    print(f"x = {x} | Approx (N=15): {approx:.4f} | Exact: {exact:.4f}")

print("-" * 40)

# PART 2: Power Series
def power_series(x, coefficients):
    """Evaluate P_N(x) with given coefficients"""
    result = 0.0
    for k, a_k in enumerate(coefficients):
        result += a_k * (x ** k)
    return result

# Testing Part 2
coeffs = [2.0, 3.0, 4.0]
x_test = 2.0
result_p2 = power_series(x_test, coeffs)
print(f"Power Series Result: {result_p2}")
import math

def sin_maclaurin(theta, N):
    """Approximate sin(theta) with N terms using Maclaurin series"""
    result = 0.0
    for n in range(N):
        sign = (-1) ** n
        factorial = math.factorial(2 * n + 1)
        result += sign * (theta ** (2 * n + 1)) / factorial
    return result
# Testing Maclaurin series for theta = 10 degrees with 1 to 4 terms
theta_deg = 10
theta_rad = math.radians(theta_deg)
exact_val = math.sin(theta_rad)

print(f"\nExact sin({theta_deg}°): {exact_val:.6f}")
for N in range(1, 5):
    approx_val = sin_maclaurin(theta_rad, N)
    print(f"Terms: {N} | Maclaurin Approx: {approx_val:.6f}")
    # PART 4: Engineering Investigation
L = 20.0  # structural length in meters
angles_deg = [1, 2, 5, 10, 15, 20, 30]
term_counts = [1, 2, 3, 4]

print("\n--- PART 4: ENGINEERING INVESTIGATION TABLES ---")
for N in range(1, 5):
    print(f"\n--- Maclaurin Approximation with N = {N} terms ---")
    print(f"{'Angle (deg)':<12} | {'Exact y':<10} | {'Approx y':<10} | {'Abs Error':<12} | {'% Error':<10}")
    print("-" * 62)
    
    for deg in angles_deg:
        rad = math.radians(deg)
        exact_y = L * math.sin(rad)
        
        # Approximate sin(theta) and then calculate y
        approx_sin = sin_maclaurin(rad, N)
        approx_y = L * approx_sin
        
        abs_error = abs(exact_y - approx_y)
        pct_error = (abs_error / abs(exact_y)) * 100 if exact_y != 0 else 0.0
        
        print(f"{deg:<12} | {exact_y:<10.4f} | {approx_y:<10.4f} | {abs_error:<12.5f} | {pct_error:<10.4f}%")
        # PART 5: Taylor Series Expansion centered at a = 10 degrees
def sin_taylor(theta, a, N):
    """Approximate sin(theta) using Taylor series centered at a"""
    result = 0.0
    sin_a, cos_a = math.sin(a), math.cos(a)
    
    for n in range(N):
        # Derivatives of sin(theta) cycle every 4 terms: sin, cos, -sin, -cos
        derivative_pattern = n % 4
        if derivative_pattern == 0:
            f_deriv = sin_a
        elif derivative_pattern == 1:
            f_deriv = cos_a
        elif derivative_pattern == 2:
            f_deriv = -sin_a
        else:
            f_deriv = -cos_a
            
        term = f_deriv * ((theta - a) ** n) / math.factorial(n)
        result += term
        
    return result
# Test Taylor series centered at a = 10 degrees
expansion_angle_deg = 10
a_rad = math.radians(expansion_angle_deg)

test_deg = 12
test_rad = math.radians(test_deg)

exact = math.sin(test_rad)
taylor_approx = sin_taylor(test_rad, a_rad, 4)

print(f"\nTesting Taylor Series centered at {expansion_angle_deg}° evaluated at {test_deg}°:")
print(f"Exact sin({test_deg}°): {exact:.6f}")
print(f"Taylor Approx (N=4): {taylor_approx:.6f}")
import matplotlib.pyplot as plt

# PART 6: Error Tolerance Analysis (< 0.1% error)
print("\n--- PART 6: TERMS NEEDED FOR < 0.1% ERROR ---")
print(f"{'Angle (deg)':<12} | {'Maclaurin Terms':<16} | {'Taylor (a=10°) Terms'}")
print("-" * 50)

for deg in angles_deg:
    rad = math.radians(deg)
    
    # Find Maclaurin terms needed
    mac_terms = 0
    for N in range(1, 10):
        approx = sin_maclaurin(rad, N)
        err = (abs(math.sin(rad) - approx) / math.sin(rad)) * 100
        if err < 0.1:
            mac_terms = N
            break
            
    # Find Taylor terms needed (centered at 10 deg)
    tay_terms = 0
    a_rad = math.radians(10)
    for N in range(1, 10):
        approx = sin_taylor(rad, a_rad, N)
        err = (abs(math.sin(rad) - approx) / math.sin(rad)) * 100
        if err < 0.1:
            tay_terms = N
            break
            
    print(f"{deg:<12} | {mac_terms:<16} | {tay_terms}")

# PART 7: Generating Required Plots
angles_dense_deg = range(1, 31)
angles_dense_rad = [math.radians(d) for d in angles_dense_deg]

# 1. Convergence Plot (% error vs terms for different angles)
plt.figure(figsize=(8, 5))
for deg in [5, 15, 30]:
    rad = math.radians(deg)
    errors = []
    term_range = range(1, 6)
    for N in term_range:
        approx = sin_maclaurin(rad, N)
        err = (abs(math.sin(rad) - approx) / math.sin(rad)) * 100
        errors.append(err)
    plt.plot(term_range, errors, marker='o', label=f'Angle = {deg}°')

plt.axhline(0.1, color='red', linestyle='--', label='0.1% Tolerance Limit')
plt.title('Maclaurin Convergence: Error vs. Number of Terms')
plt.xlabel('Number of Terms (N)')
plt.ylabel('Percentage Error (%)')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# --- ADDITIONAL DELIVERABLES: Function & Error Comparison Plots ---

# 3. Function Comparison Plot (Exact vs Maclaurin vs Taylor)
plt.figure(figsize=(10, 5))
angles_deg_range = range(0, 31)
angles_rad_range = [math.radians(d) for d in angles_deg_range]

exact_vals = [20 * math.sin(r) for r in angles_rad_range]
mac_vals = [20 * sin_maclaurin(r, 2) for r in angles_rad_range]
tay_vals = [20 * sin_taylor(r, math.radians(10), 2) for r in angles_rad_range]

plt.plot(angles_deg_range, exact_vals, 'k-', linewidth=2, label='Exact y = L*sin(theta)')
plt.plot(angles_deg_range, mac_vals, 'b--', label='Maclaurin (N=2)')
plt.plot(angles_deg_range, tay_vals, 'r:', label='Taylor a=10° (N=2)')
plt.title('Function Comparison: Exact vs. Series Approximations (L = 20m)')
plt.xlabel('Angle (degrees)')
plt.ylabel('Vertical Component y (m)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Error Comparison Plot (Maclaurin vs Taylor Percentage Errors)
plt.figure(figsize=(10, 5))
mac_errors = []
tay_errors = []
a_rad = math.radians(10)

for d in angles_deg_range[1:]: # skip 0 to avoid division by zero
    r = math.radians(d)
    ex = math.sin(r)
    m_err = (abs(ex - sin_maclaurin(r, 2)) / ex) * 100
    t_err = (abs(ex - sin_taylor(r, a_rad, 2)) / ex) * 100
    mac_errors.append(m_err)
    tay_errors.append(t_err)

plt.plot(list(angles_deg_range)[1:], mac_errors, 'b-', label='Maclaurin Error (N=2)')
plt.plot(list(angles_deg_range)[1:], tay_errors, 'r-', label='Taylor (a=10°) Error (N=2)')
plt.axhline(0.1, color='green', linestyle='--', label='0.1% Tolerance Threshold')
plt.title('Error Comparison: Maclaurin vs. Taylor Series (N=2 terms)')
plt.xlabel('Angle (degrees)')
plt.ylabel('Percentage Error (%)')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# --- 5. WRITTEN RECOMMENDATION ---
print("\n" + "="*70)
print("PART 7: FINAL ENGINEERING RECOMMENDATION")
print("="*70)
print("""
1. Number of Terms Required:
   - For angles up to 30°, using a Maclaurin series with N = 2 terms 
     consistently satisfies the strict < 0.1% error tolerance requirement.
   - For operations tightly clustered around 10°, a Taylor series centered 
     at a = 10° achieves high accuracy with even fewer terms.

2. Percentage Error Achieved:
   - Across the 1° to 30° structural range, a 2-term Maclaurin approximation 
     keeps the percentage error well below 0.07% (dropping to 0.00% for smaller angles).

3. Convergence Behavior:
   - The series exhibits rapid exponential convergence. Each added term 
     reduces the error by multiple orders of magnitude, making higher-order 
     terms computationally redundant for standard structural ranges.

4. Computational Simplicity vs. Accuracy Tradeoff:
   - While a 1-term small angle approximation (sin(theta) approx theta) is 
     simpler, it breaks the 0.1% tolerance threshold past 5°. 
   - A 2-term Maclaurin or Taylor series provides the optimal engineering 
     balance: negligible computational overhead paired with high precision.

5. Valid Angle Range & Final Decision:
   - Recommendation: Use the 2-term Maclaurin series for general structural 
     angles ranging between 0° and 30°. It completely fulfills accuracy specs 
     without requiring complex expansion shifting.
""")
print("="*70)