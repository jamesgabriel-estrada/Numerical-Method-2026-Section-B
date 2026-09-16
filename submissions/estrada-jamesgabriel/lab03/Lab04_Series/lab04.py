import matplotlib.pyplot as plt
import numpy as np

# Ensure you install required libraries first:
# pip install matplotlib numpy python-pptx

# --- EXERCISE 1: Convergence of (1 + 1/n)^n to e ---
labels = [
    "yearly",
    "twice a year",
    "quarterly",
    "monthly",
    "weekly",
    "daily",
    "hourly",
    "every minute",
    "every second",
    "every millisecond",
    "every microsecond",
    "every nanosecond",
]
n_values = [
    1,
    2,
    4,
    12,
    52,
    365,
    365 * 24,
    365 * 24 * 60,
    365 * 24 * 3600,
    365 * 24 * 3600 * 1e3,
    365 * 24 * 3600 * 1e6,
    365 * 24 * 3600 * 1e9,
]
values = [(1 + 1 / n) ** n for n in n_values]
errors = [abs(v - np.e) for v in values]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.bar(labels, values, color="royalblue")
ax1.axhline(np.e, color="red", linestyle="--", label=f"e = {np.e:.5f}")
ax1.set_title("Exercise 1: Value per compounding period")
ax1.set_xticklabels(labels, rotation=45, ha="right")
ax1.legend()

ax2.bar(labels, errors, color="darkorange")
ax2.set_yscale("log")
ax2.set_title("Exercise 1: Error shrinks like e/(2n)")
ax2.set_xticklabels(labels, rotation=45, ha="right")
plt.tight_layout()
plt.savefig("exercise_1.png", dpi=300)
plt.close()

# --- EXERCISE 2: Difference Quotient Settling to ln(a) ---
h_vals = [0.1, 0.01, 0.001, 0.0001, 1e-05, 1e-06, 1e-07]
bases = [2, np.e, 3]
base_labels = ["a = 2", "a = e", "a = 3"]
limits = [np.log(2), 1.0, np.log(3)]

x = np.arange(len(h_vals))
width = 0.25
fig, ax = plt.subplots(figsize=(10, 6))

for i, base in enumerate(bases):
  y_vals = [(base**h - 1) / h for h in h_vals]
  ax.bar(
      x + i * width,
      y_vals,
      width,
      label=f"{base_labels[i]} (ln a = {limits[i]:.4f})",
  )

ax.set_xticks(x + width)
ax.set_xticklabels([str(h) for h in h_vals])
ax.set_title("Exercise 2: (a^h - 1)/h settling to ln(a)")
ax.legend()
plt.tight_layout()
plt.savefig("exercise_2.png", dpi=300)
plt.close()

# --- EXERCISE 3: Taylor Series for e^x up to 10,000 terms ---
N = 10000
terms = np.arange(1, N + 1)
partial_sums, current_sum, factorial = [], 0.0, 1.0
for n in range(1, N + 1):
  if n > 1:
    factorial *= n - 1
  current_sum += 1.0 / factorial
  partial_sums.append(current_sum)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(terms[:100], partial_sums[:100], color="purple", marker="o")
ax1.axhline(np.e, color="red", linestyle="--", label=f"e = {np.e:.5f}")
ax1.set_title("Exercise 3: Partial Sums Histogram / Plot")
ax1.legend()

errors_ex3 = [abs(s - np.e) for s in partial_sums]
ax2.loglog(terms, errors_ex3, color="teal")
ax2.set_title("Exercise 3: Accuracy Trend (Log-Log)")
ax2.set_xlabel("Number of terms N")
ax2.set_ylabel("Absolute Error")
plt.tight_layout()
plt.savefig("exercise_3.png", dpi=300)
plt.close()

# --- HTML DASHBOARD GENERATION ---
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Numerical Methods Laboratory Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; color: #333; }
        h1, h2 { color: #2c3e50; }
        .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Numerical Methods Laboratory Activity Dashboard</h1>
    <div class="card">
        <h2>Exercise 1: Convergence of (1 + 1/n)^n to e</h2>
        <p>Evaluated compound frequencies scaling from yearly down to nanoseconds.</p>
        <img src="exercise_1.png" alt="Exercise 1 Plot">
    </div>
    <div class="card">
        <h2>Exercise 2: Difference Quotient Settling to ln(a)</h2>
        <p>Demonstrates difference quotients for bases a=2, e, 3 as h shrinks to 1e-07.</p>
        <img src="exercise_2.png" alt="Exercise 2 Plot">
    </div>
    <div class="card">
        <h2>Exercise 3: Taylor Series Expansion for e^x</h2>
        <p>Partial sums expansion up to N = 10,000 terms with log-log accuracy trend.</p>
        <img src="exercise_3.png" alt="Exercise 3 Plot">
    </div>
</body>
</html>
"""

with open("dashboard.html", "w") as f:
  f.write(html_content)

# --- PPTX PRESENTATION GENERATION ---
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Slide 1: Title Slide
slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(slide_layout)
slide.shapes.title.text = (
    "Numerical Methods Laboratory Activity\nSeries and Limits Convergence"
)
slide.placeholders[1].text = (
    "Section A | Complete Python Implementation & Results"
)


# Helper function to add image slides
def add_image_slide(title_text, img_path):
  blank_layout = prs.slide_layouts[5]
  slide = prs.slides.add_slide(blank_layout)
  title_shape = slide.shapes.title
  title_shape.text = title_text
  slide.shapes.add_picture(
      img_path, Inches(0.8), Inches(1.5), width=Inches(8.5)
  )


add_image_slide("Exercise 1: Convergence to e", "exercise_1.png")
add_image_slide("Exercise 2: Difference Quotient Settling", "exercise_2.png")
add_image_slide("Exercise 3: Taylor Series Expansion", "exercise_3.png")

prs.save("Numerical_Methods_Lab.pptx")
print(
    "All deliverables (3 PNGs, dashboard.html, and Numerical_Methods_Lab.pptx)"
    " generated successfully!"
)