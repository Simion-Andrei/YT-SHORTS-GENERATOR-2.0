from src.video_renderer import VideoRenderer
from src.audio_generator import AudioGenerator

if __name__ == "__main__":
    idx = 2
    scripts = [
        {
            "msg": [
                "What on earth are you doing? That's enough protein to feed a small nation!",
                "Gotta get my pre-workout nutrition, Stewie! Building these massive guns requires maximum protein!",
                "You complete buffoon! Pre-workout nutrition isn't about protein bombs. It's about accessible energy and moderate protein!",
                "But the guy at GNC said I need 80 grams of protein before and after...",
                "Listen carefully. Pre-workout: 15-30g protein with carbs 1-2 hours before training. Carbs fuel performance, moderate protein prevents breakdown. Simple!",
                "So this 700-calorie monster energy drink is perfect?",
                "Absolutely not! Pre-workout should be easily digestible - think banana with greek yogurt or toast with eggs. Avoid excess fat and fiber that slow digestion.",
                "Now I definetly need all the protein, right?",
                "Post-workout is when protein matters most. Your anabolic window is open for about 24 hours, but having 20-40g protein within 2 hours optimizes recovery.",
                "So... protein after, not before?",
                "Both matter, but differently! Pre-workout: moderate protein with carbs for energy. Post-workout: higher protein with carbs to replenish glycogen and rebuild muscle.",
                "So what's the perfect post-workout meal?",
                "Protein source with faster digestion - shake, chicken, eggs - plus quick carbs like rice or potatoes. 3:1 carb-to-protein ratio if you did cardio, 2:1 for strength training. And timing matters less than total daily nutrition!",
                "Don't forget to like and subscribe for more gym tips!"

            ],
            "img": {
                0: "assets/images/img.png",
                4: "assets/images/img_1.png",
                5: "assets/images/img_2.png",
            }
        },
    ]

    for i, script in enumerate(scripts):
        ag = AudioGenerator("stewie", "peter", script["msg"])
        ag.generate_audio()

        if idx == 1:
            vr = VideoRenderer("assets/characters/rickandmorty/rick.png", "assets/characters/rickandmorty/morty.png", "assets/characters/rickandmorty/rick_pointing.webp", "assets/characters/rickandmorty/morty_pointing.png", script)
            vr.render_video(i)
        elif idx == 2:
            vr = VideoRenderer("assets/characters/musclefamilyguy/stewie.webp", "assets/characters/musclefamilyguy/peter.png", "assets/characters/musclefamilyguy/stewie_pointing.png", "assets/characters/musclefamilyguy/peter_pointing.png", script)
            vr.render_video(i)