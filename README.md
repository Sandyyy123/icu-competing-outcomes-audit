> **Proprietary - All Rights Reserved.** Licensed to Sandeep Grover. No reuse, copying, modification, or distribution without prior written permission. See LICENSE.

# ICU competing-outcome audit: synthetic teaching fixture
A narrow, reproducible first-event cumulative-incidence calculation. No clinical data.
Run: python3 competing_outcomes.py
Test: python3 -m unittest -v

Demonstrates why censoring death and interpreting 1-KM as probability of discharge is incorrect.
Supports right censoring, a shared time-zero and tied events; events precede censoring at tied times.
No delayed entry, weights, repeated admissions, covariate regression or confidence intervals.
This is not a clinical model or a replacement for a validated survival-analysis package.
Method reference: https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf
