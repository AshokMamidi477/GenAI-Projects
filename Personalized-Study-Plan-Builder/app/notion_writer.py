"""notion_writer.py — Markdown plan to Notion blocks"""
import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

print("TOKEN:", os.getenv("NOTION_TOKEN"))
print("PARENT PAGE:", PARENT_PAGE_ID)

def _make_block(btype, text):
    return {"object":"block","type":btype,
            btype:{"rich_text":[{"type":"text","text":{"content":text[:2000]}}]}}

def _md_to_blocks(md):
    blocks = []
    for line in md.splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith("## "): blocks.append(_make_block("heading_2", line[3:]))
        elif line.startswith("### "): blocks.append(_make_block("heading_3", line[4:]))
        elif line.startswith("- "): blocks.append(_make_block("bulleted_list_item", line[2:]))
        else: blocks.append(_make_block("paragraph", line))
    return blocks

def save_plan_to_notion(topic, target_date, plan_md):
    page = notion.pages.create(
        parent={"page_id": PARENT_PAGE_ID},
        properties={"title":{"title":[{"text":{"content":f"{topic} Study Plan — {target_date}"}}]}},
    )
    blocks = _md_to_blocks(plan_md)
    for i in range(0, len(blocks), 100):
        notion.blocks.children.append(block_id=page["id"], children=blocks[i:i+100])
    return page.get("url", "")
