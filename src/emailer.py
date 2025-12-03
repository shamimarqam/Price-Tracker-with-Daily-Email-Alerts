import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT


def build_html_email(summary, drops):
    """Create an HTML email body with summary + price-drop alerts."""

    # Daily summary table
    rows = ""
    for item in summary:
        rows += f"""
            <tr>
                <td>{item['product_name']}</td>
                <td>{item['site']}</td>
                <td>₹{item['price']}</td>
                <td>{item['date']}</td>
            </tr>
        """

    summary_table = f"""
        <h3>Daily Price Summary</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Product</th>
                <th>Site</th>
                <th>Price</th>
                <th>Date</th>
            </tr>
            {rows}
        </table>
        <br>
    """

    # Price-drop section
    if drops:
        drop_rows = ""
        for d in drops:
            drop_rows += f"""
                <tr>
                    <td>{d['product_name']}</td>
                    <td>{d['site']}</td>
                    <td>₹{d['old_price']}</td>
                    <td>₹{d['new_price']}</td>
                    <td><a href="{d['url']}">View Product</a></td>
                </tr>
            """

        drop_table = f"""
            <h3 style="color:red;">Price Drop Alerts</h3>
            <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
                <tr>
                    <th>Product</th>
                    <th>Site</th>
                    <th>Old Price</th>
                    <th>New Price</th>
                    <th>Link</th>
                </tr>
                {drop_rows}
            </table>
            <br>
        """
    else:
        drop_table = "<p>No price drops today.</p><br>"

    return summary_table + drop_table


def send_email(summary, drops):
    """Send price report email using SMTP."""
    html_content = build_html_email(summary, drops)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Price Tracking Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


if __name__ == "__main__":
    # For direct testing
    # Mock data
    summary = [
        {"product_name": "Test Product", "site": "amazon", "price": 999, "date": "2025-12-02"}
    ]
    drops = [
        {"product_name": "Test Product", "site": "amazon", "old_price": 1200, "new_price": 999, "url": "http://amazon.in"}
    ]

    send_email(summary, drops)