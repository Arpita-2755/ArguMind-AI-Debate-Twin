from services.moderator_service import ModeratorService

plan = ModeratorService.create_plan(
    "Should AI replace software engineers?",
    "Oppose"
)

print("\n========== GENERATED PLAN ==========\n")
print(plan)
print(type(plan))