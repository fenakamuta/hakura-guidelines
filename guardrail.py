# Import Guard and Validator
from guardrails.hub import RestrictToTopic
from guardrails import Guard

# Setup Guard
guard = Guard().use(
    RestrictToTopic(
        valid_topics=["health", "accident", "patient", "doctor"],
        # invalid_topics=["music"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="exception"
    )
)

# guard.validate("""
# In Super Bowl LVII in 2023, the Chiefs clashed with the Philadelphia Eagles in a fiercely contested battle, ultimately emerging victorious with a score of 38-35.
# """)  # Validator passes

guard.validate("""
Sou jogador de futebol.
""")  # Validator fails