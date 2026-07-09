"""app.py — Streamlit UI for invoice extraction"""

import pandas as pd
import streamlit as st
from pdf_utils import pdf_to_base64_images
from extractor import extract_invoice

st.set_page_config(page_title="Invoice Data Extractor", page_icon="💰", layout="wide")
st.title("💰 Invoice Data Extractor")
st.caption("Upload an invoice PDF or fetch invoices from Gmail — extract structured data using Google Gemini.")

# --- Shared display function ---
def display_invoice_data(data: dict):
    """Render extracted invoice data in the Streamlit UI."""
    st.subheader("Invoice Details")
    meta_cols = st.columns(3)
    meta_cols[0].metric("Vendor", data.get("vendor_name") or "—")
    meta_cols[1].metric("Invoice #", data.get("invoice_number") or "—")
    meta_cols[2].metric("Currency", data.get("currency") or "—")

    date_cols = st.columns(3)
    date_cols[0].metric("Invoice Date", data.get("invoice_date") or "—")
    date_cols[1].metric("Due Date", data.get("due_date") or "—")
    date_cols[2].metric("Grand Total", data.get("grand_total") or "—")

    # Editable line items table
    st.subheader("Line Items (editable)")
    line_items = data.get("line_items", [])
    if line_items:
        df = pd.DataFrame(line_items)
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    else:
        st.info("No line items extracted.")
        edited_df = pd.DataFrame()

    # Totals
    st.subheader("Totals")
    total_cols = st.columns(3)
    total_cols[0].metric("Subtotal", data.get("subtotal") or "—")
    total_cols[1].metric("Tax", f"{data.get('tax_amount') or '—'} ({data.get('tax_rate') or '—'})")
    total_cols[2].metric("Grand Total", data.get("grand_total") or "—")

    # CSV export
    if not edited_df.empty:
        csv = edited_df.to_csv(index=False)
        st.download_button(
            label="⬇ Download Line Items as CSV",
            data=csv,
            file_name=f"invoice_{data.get('invoice_number', 'export')}.csv",
            mime="text/csv",
        )


# --- Tabs ---
tab_upload, tab_gmail = st.tabs(["📄 Upload PDF", "📧 Gmail Integration"])

# ============================================================
# TAB 1: Manual PDF Upload (existing functionality)
# ============================================================
with tab_upload:
    uploaded_file = st.file_uploader(
        "Upload Invoice PDF (max 10 MB, up to 3 pages processed)",
        type=["pdf", "image"],
    )

    if uploaded_file:
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > 10:
            st.error("File is too large. Please upload a file under 10 MB.")
            st.stop()

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.markdown("**File details**")
            st.caption(f"Name: `{uploaded_file.name}`")
            st.caption(f"Size: `{file_size_mb:.2f} MB`")
            extract_btn = st.button("🔍 Extract Invoice Data", type="primary", use_container_width=True)
            retry_btn = st.button("🔄 Retry Extraction", use_container_width=True)

        with col2:
            if extract_btn or retry_btn:
                with st.spinner("Rendering PDF pages..."):
                    try:
                        b64_images = pdf_to_base64_images(uploaded_file.getvalue())
                        st.caption(f"✅ {len(b64_images)} page(s) rendered")
                    except ValueError as e:
                        st.error(str(e))
                        st.stop()

                with st.spinner("Extracting data with Gemini Vision..."):
                    try:
                        data = extract_invoice(b64_images)
                    except Exception as e:
                        st.error(f"Extraction failed: {e}")
                        st.stop()

                display_invoice_data(data)

# ============================================================
# TAB 2: Gmail Integration
# ============================================================
with tab_gmail:
    st.markdown("""
    **Auto-process invoice attachments from your Gmail inbox.**
    
    This connects to your Gmail account via OAuth 2.0 (read-only access) and searches 
    for emails with PDF attachments that look like invoices.
    """)

    # Setup instructions in an expander
    with st.expander("⚙️ Setup Instructions", expanded=False):
        st.markdown("""
        **One-time setup required:**
        
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a project (or use an existing one)
        3. Enable the **Gmail API**
        4. Go to **APIs & Services → Credentials**
        5. Create an **OAuth 2.0 Client ID** (Desktop application type)
        6. Download the JSON file and save it as:
           ```
           credentials/client_secret.json
           ```
        7. On first connection, a browser window will open for you to authorize access.
        
        Your token is stored locally at `credentials/token.json` and refreshes automatically.
        """)

    st.divider()

    # Search configuration
    col_search, col_opts = st.columns([2, 1])
    with col_search:
        search_query = st.text_input(
            "Gmail search query",
            value="has:attachment filename:pdf subject:invoice",
            help="Uses Gmail search syntax. Examples: 'from:vendor@company.com', 'newer_than:7d', 'subject:invoice'"
        )
    with col_opts:
        max_emails = st.number_input("Max emails to fetch", min_value=1, max_value=50, value=10)

    fetch_btn = st.button("📧 Fetch Invoice Emails", type="primary", use_container_width=True)

    if fetch_btn:
        try:
            from gmail_client import fetch_invoice_emails, get_pdf_attachments

            with st.spinner("Connecting to Gmail and searching..."):
                service, emails = fetch_invoice_emails(
                    query=search_query, max_results=max_emails
                )

            if not emails:
                st.warning("No emails found matching your search query.")
            else:
                st.success(f"Found {len(emails)} email(s) with potential invoices.")
                st.session_state["gmail_service"] = service
                st.session_state["gmail_emails"] = emails

        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Gmail connection failed: {e}")

    # Display fetched emails
    if "gmail_emails" in st.session_state and st.session_state["gmail_emails"]:
        st.subheader("📬 Emails with Invoice Attachments")

        for i, email in enumerate(st.session_state["gmail_emails"]):
            with st.container():
                ecol1, ecol2, ecol3 = st.columns([3, 2, 1])
                ecol1.markdown(f"**{email['subject']}**")
                ecol2.caption(f"From: {email['from']}")
                ecol3.caption(email["date"])

                process_btn = st.button(
                    f"🔍 Process", key=f"process_{email['id']}",
                    use_container_width=True
                )

                if process_btn:
                    from gmail_client import get_pdf_attachments

                    service = st.session_state["gmail_service"]

                    with st.spinner(f"Downloading attachments from: {email['subject']}..."):
                        attachments = get_pdf_attachments(service, email["id"])

                    if not attachments:
                        st.warning("No PDF attachments found in this email.")
                    else:
                        for att in attachments:
                            st.markdown(f"---\n**Processing:** `{att['filename']}`")

                            with st.spinner(f"Rendering {att['filename']}..."):
                                try:
                                    b64_images = pdf_to_base64_images(att["data"])
                                    st.caption(f"✅ {len(b64_images)} page(s) rendered")
                                except ValueError as e:
                                    st.error(f"PDF error: {e}")
                                    continue

                            with st.spinner("Extracting invoice data with Gemini Vision..."):
                                try:
                                    data = extract_invoice(b64_images)
                                except Exception as e:
                                    st.error(f"Extraction failed: {e}")
                                    continue

                            display_invoice_data(data)

                st.divider()
