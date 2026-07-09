"""Generate a sample invoice PDF using PyMuPDF (fitz) for testing."""

import fitz  # PyMuPDF

def create_sample_invoice(output_path: str = "sample/sample_invoice.pdf"):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4

    # Colors
    black = (0, 0, 0)
    gray = (0.4, 0.4, 0.4)
    dark_blue = (0.1, 0.2, 0.5)

    # Header
    page.insert_text((50, 50), "INVOICE", fontsize=28, fontname="helv", color=dark_blue)
    
    # Company info (top right)
    page.insert_text((350, 50), "Acme Solutions Ltd.", fontsize=12, fontname="helv", color=black)
    page.insert_text((350, 66), "123 Business Park, Suite 400", fontsize=9, fontname="helv", color=gray)
    page.insert_text((350, 80), "San Francisco, CA 94105", fontsize=9, fontname="helv", color=gray)
    page.insert_text((350, 94), "Phone: (415) 555-0198", fontsize=9, fontname="helv", color=gray)
    page.insert_text((350, 108), "Email: billing@acmesolutions.com", fontsize=9, fontname="helv", color=gray)

    # Divider line
    page.draw_line((50, 125), (545, 125), color=dark_blue, width=1.5)

    # Invoice details
    y = 150
    page.insert_text((50, y), "Invoice Number:", fontsize=10, fontname="helv", color=gray)
    page.insert_text((170, y), "INV-2024-00742", fontsize=10, fontname="helv", color=black)
    
    y += 18
    page.insert_text((50, y), "Invoice Date:", fontsize=10, fontname="helv", color=gray)
    page.insert_text((170, y), "2024-11-15", fontsize=10, fontname="helv", color=black)
    
    y += 18
    page.insert_text((50, y), "Due Date:", fontsize=10, fontname="helv", color=gray)
    page.insert_text((170, y), "2024-12-15", fontsize=10, fontname="helv", color=black)

    # Bill To
    y += 40
    page.insert_text((50, y), "Bill To:", fontsize=10, fontname="helv", color=dark_blue)
    y += 16
    page.insert_text((50, y), "TechStart Inc.", fontsize=10, fontname="helv", color=black)
    y += 14
    page.insert_text((50, y), "456 Innovation Drive", fontsize=9, fontname="helv", color=gray)
    y += 14
    page.insert_text((50, y), "Austin, TX 78701", fontsize=9, fontname="helv", color=gray)

    # Table header
    y += 40
    page.draw_rect(fitz.Rect(50, y - 5, 545, y + 15), color=dark_blue, fill=dark_blue)
    page.insert_text((55, y + 9), "Description", fontsize=9, fontname="helv", color=(1, 1, 1))
    page.insert_text((300, y + 9), "Qty", fontsize=9, fontname="helv", color=(1, 1, 1))
    page.insert_text((370, y + 9), "Unit Price", fontsize=9, fontname="helv", color=(1, 1, 1))
    page.insert_text((470, y + 9), "Total", fontsize=9, fontname="helv", color=(1, 1, 1))

    # Line items
    items = [
        ("Web Application Development", "1", "$4,500.00", "$4,500.00"),
        ("UI/UX Design Services", "2", "$1,200.00", "$2,400.00"),
        ("Cloud Infrastructure Setup", "1", "$800.00", "$800.00"),
        ("Monthly Maintenance (Nov 2024)", "1", "$350.00", "$350.00"),
    ]

    y += 25
    for desc, qty, unit, total in items:
        page.insert_text((55, y), desc, fontsize=9, fontname="helv", color=black)
        page.insert_text((310, y), qty, fontsize=9, fontname="helv", color=black)
        page.insert_text((370, y), unit, fontsize=9, fontname="helv", color=black)
        page.insert_text((470, y), total, fontsize=9, fontname="helv", color=black)
        y += 20
        page.draw_line((50, y - 6), (545, y - 6), color=(0.85, 0.85, 0.85), width=0.5)

    # Totals
    y += 20
    page.draw_line((350, y - 5), (545, y - 5), color=dark_blue, width=1)
    
    y += 10
    page.insert_text((370, y), "Subtotal:", fontsize=10, fontname="helv", color=gray)
    page.insert_text((470, y), "$8,050.00", fontsize=10, fontname="helv", color=black)
    
    y += 20
    page.insert_text((370, y), "Tax (10%):", fontsize=10, fontname="helv", color=gray)
    page.insert_text((470, y), "$805.00", fontsize=10, fontname="helv", color=black)
    
    y += 25
    page.draw_line((350, y - 5), (545, y - 5), color=dark_blue, width=1.5)
    y += 10
    page.insert_text((370, y), "Grand Total:", fontsize=12, fontname="helv", color=dark_blue)
    page.insert_text((470, y), "$8,855.00", fontsize=12, fontname="helv", color=dark_blue)

    # Currency note
    y += 30
    page.insert_text((370, y), "Currency: USD", fontsize=9, fontname="helv", color=gray)

    # Footer
    page.draw_line((50, 780), (545, 780), color=(0.85, 0.85, 0.85), width=0.5)
    page.insert_text((50, 800), "Payment Terms: Net 30 | Please include invoice number with payment.", fontsize=8, fontname="helv", color=gray)
    page.insert_text((50, 815), "Thank you for your business!", fontsize=8, fontname="helv", color=gray)

    doc.save(output_path)
    doc.close()
    print(f"✅ Sample invoice saved to: {output_path}")


if __name__ == "__main__":
    create_sample_invoice()
