from diary.models import Question

questions = [
    "Happenings of the past 6 months.",
    "Something that has made you think in the past few months (song/movie/kazhchakal).",
    "Something or someone you hate at the moment.",
    "What has surprised you about yourself or others?",
    "What have you let go of (physically or emotionally)?",
    "Is there something you wish you'd done differently?",
    "Plans for the next 6 months.",
    "Superpower for the next 6 months: If you could have one, what would it be?",
    "Bucket list.",
    "Guiding word/phrase (for the next six months).",
    "What is your comfort zone? Have you stepped out of it?",
    "Mind and body health: Are you looking after yourself?",
    "What's working well in your routine, and what needs tweaking?",
    "Small, everyday experiences that made you happy.",
    "Moment/person you are grateful or thankful for.",
    "What's one good decision you've made with money?",
    "What's something you splurged on that brought joy?",
    "Any new friendships or networks formed?",
    "Who or what has inspired you lately?",
    "Are you spending your time the way you'd like to?",
    "Letter/note to your future self for the next six months.",
    "Photos to symbolize your journey."
]

objects = [
    Question(number=i + 1, question=q)
    for i, q in enumerate(questions)
]

Question.objects.bulk_create(objects)

print(f"{len(objects)} numbered questions imported successfully.")
