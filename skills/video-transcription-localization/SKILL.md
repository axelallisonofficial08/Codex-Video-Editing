---
name: video-transcription-localization
description: Create, correct, translate, time, and render captions or subtitles for speech or lyrics in a video. Use when the user requests transcription, captions, translation, dubbing support, or localized delivery.
---

# Video transcription and localization

Inspect the audio and determine language, speakers, and whether the request calls for verbatim captions, cleaned captions, translated subtitles, or a dub script. Use an available ASR tool when useful, then review names, lyrics, fast speech, and low-confidence spans against audio. Do not treat unreviewed ASR as ground truth.

Time captions to audible words or phrases, including pauses and speaker changes. Keep readable line lengths and sufficient on-screen time; check against picture cuts and action. Preserve meaning, tone, and proper nouns during translation, and mark genuinely ambiguous phrases for review rather than inventing certainty.

Produce an editable caption file such as SRT or VTT when appropriate, and burn subtitles only when requested or required by delivery. Verify timing and readability in the rendered video. Do not replace an existing soundtrack as a side effect of caption work.
