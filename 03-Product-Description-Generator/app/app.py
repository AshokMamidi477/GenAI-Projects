"""
app.py
Gradio UI for the Product Description Generator.
"""

import asyncio
import os
import gradio as gr
from dotenv import load_dotenv
from prompt_templates import build_prompt, parse_response
from notion_writer import save_to_notion
from openai import AsyncOpenAI

load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# client = genai.GenerativeModel("gemini-pro")


client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

TONES = ["Professional", "Playful", "Urgency"]
CATEGORIES = [
    "Electronics", "Clothing & Apparel", "Food & Beverage",
    "Beauty & Skincare", "Home & Garden", "Sports & Outdoors",
    "Books & Media", "Toys & Games", "Tools & Hardware", "Digital Products",
]


async def generate_single(prompt):
    response = await client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.75,
        max_tokens=500,
    )

    return response.choices[0].message.content


async def generate_all(title, category, features, audience, keywords):
    prompts = [
        build_prompt(title, category, features, audience, keywords, tone)
        for tone in TONES
    ]
    return await asyncio.gather(*[generate_single(p) for p in prompts])


def on_generate(title, category, features, audience, keywords):
    if not title.strip():
        return ["Please enter a product title."] * 6
    raw_results = asyncio.run(generate_all(title, category, features, audience, keywords))
    outputs = []
    for raw in raw_results:
        desc, meta = parse_response(raw)
        outputs.extend([desc, meta])
    return outputs


def on_save(product, tone_choice, desc_pro, desc_play, desc_urg):
    mapping = {"Professional": desc_pro, "Playful": desc_play, "Urgency": desc_urg}
    desc = mapping.get(tone_choice, desc_pro)
    url = save_to_notion(product, desc, tone_choice, "")
    return f"Saved to Notion: {url}" if url else "Saved to Notion"


with gr.Blocks(title="Product Description Generator") as demo:
    gr.Markdown("# Product Description Generator")
    gr.Markdown("Generate 3 tone-distinct, SEO-ready descriptions in parallel.")

    with gr.Row():
        with gr.Column(scale=1):
            title_in  = gr.Textbox(label="Product Title *")
            cat_in    = gr.Dropdown(label="Category", choices=CATEGORIES, value="Electronics")
            feat_in   = gr.Textbox(label="Key Features (one per line)", lines=4)
            aud_in    = gr.Textbox(label="Target Audience")
            kw_in     = gr.Textbox(label="Keywords (optional)")
            gen_btn   = gr.Button("Generate All 3 Variants", variant="primary")

        with gr.Column(scale=2):
            with gr.Tab("Professional"):
                desc_pro = gr.Textbox(label="Description", lines=7)
                meta_pro = gr.Textbox(label="SEO Meta (<=155 chars)")
            with gr.Tab("Playful"):
                desc_play = gr.Textbox(label="Description", lines=7)
                meta_play = gr.Textbox(label="SEO Meta (<=155 chars)")
            with gr.Tab("Urgency"):
                desc_urg = gr.Textbox(label="Description", lines=7)
                meta_urg = gr.Textbox(label="SEO Meta (<=155 chars)")

            tone_choice = gr.Radio(label="Save which tone to Notion?", choices=TONES, value="Professional")
            save_btn    = gr.Button("Save to Notion")
            save_status = gr.Textbox(label="Save Status", interactive=False)

    gen_btn.click(
        on_generate,
        inputs=[title_in, cat_in, feat_in, aud_in, kw_in],
        outputs=[desc_pro, meta_pro, desc_play, meta_play, desc_urg, meta_urg],
    )
    save_btn.click(
        on_save,
        inputs=[title_in, tone_choice, desc_pro, desc_play, desc_urg],
        outputs=[save_status],
    )

if __name__ == "__main__":
    demo.launch()
