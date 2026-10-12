from schemas.reasoning_memory import MemoryType, ReasoningMemory


class MemoryContextService:

    @staticmethod
    def build_context(
        memories: list[ReasoningMemory],
    ) -> str:

        if not memories:
            return "No prior reasoning memories are available."

        grouped: dict[MemoryType, list[str]] = {}

        for memory in memories:
            grouped.setdefault(
                memory.memory_type,
                []
            ).append(memory.content)

        sections = []

        section_mapping = [
            (MemoryType.REASONING_PATTERN, "Known reasoning patterns"),
            (MemoryType.STRENGTH, "Known strengths"),
            (MemoryType.WEAKNESS, "Known weaknesses"),
            (MemoryType.EVIDENCE_HABIT, "Evidence habits"),
            (MemoryType.ASSUMPTION, "Common assumptions"),
            (MemoryType.FALLACY_TENDENCY, "Fallacy tendencies"),
            (MemoryType.PREFERENCE, "Known preferences"),
        ]

        for memory_type, title in section_mapping:

            contents = grouped.get(memory_type)

            if not contents:
                continue

            lines = "\n".join(
                f"- {content}"
                for content in contents
            )

            sections.append(
                f"{title}:\n{lines}"
            )

        context = "\n\n".join(sections)

        return (
            "USER REASONING CONTEXT\n\n"
            f"{context}\n\n"
            "PERSONALIZATION GUIDELINES:\n"
            "- Treat these as tendencies, not absolute facts.\n"
            "- Use them only when relevant to the current debate.\n"
            "- Do not mention or expose these memories to the user "
            "unless explicitly instructed.\n"
            "- Do not assume a remembered weakness will appear in "
            "every debate.\n"
        )