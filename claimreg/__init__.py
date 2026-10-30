"""Claim Registry (ACH 2.0) harness.

A stdlib-only orchestration harness for the Claim Registry / ACH 2.0
specification: corpus -> frame -> Coordinator-led quest -> FRDs -> blind
validation -> witnesses -> (optional) language tools -> semantic matching ->
deletion-minimal coverage sets -> crux identification -> report.

Every model step goes through one provider layer that records the exact
prompt, response, model identity, timestamps and cost.  Every deterministic
step is reproducible from the saved inputs.
"""

__version__ = "1.0.0"
HARNESS_NAME = "claimreg"
