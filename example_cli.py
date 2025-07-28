#!/usr/bin/env python3
"""Example CLI for Smart Email Client."""

import sys
from datetime import datetime
from gmail_implementation.client import GmailClient
from mail_client_interface.exceptions import (
    AuthenticationError, ConnectionError, ServiceError, ConfigurationError
)


def format_email_summary(email, index):
    """Format email summary for display."""
    status_icon = "📧" if email.status.value == "unread" else "📩"
    attachment_icon = "📎" if email.has_attachments else ""
    
    print(f"\n{index}. {status_icon} {email.subject} {attachment_icon}")
    print(f"   From: {email.sender}")
    print(f"   Date: {email.date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Preview: {email.snippet[:100]}...")


def format_email_detail(email):
    """Format detailed email for display."""
    print(f"\n{'='*60}")
    print(f"From: {email.sender}")
    print(f"To: {', '.join(str(addr) for addr in email.recipients)}")
    if email.cc:
        print(f"Cc: {', '.join(str(addr) for addr in email.cc)}")
    print(f"Subject: {email.subject}")
    print(f"Date: {email.date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Status: {email.status.value.title()}")
    
    if email.attachments:
        print(f"\nAttachments ({len(email.attachments)}):")
        for att in email.attachments:
            size_kb = att.size_bytes / 1024
            print(f"  📎 {att.filename} ({size_kb:.1f} KB)")
    
    print(f"\n{'-'*60}")
    print("Body:")
    print(email.body_text or email.body_html or "(No content)")
    print(f"{'='*60}")


def main():
    """Main CLI application."""
    print("🚀 Smart Email Client")
    print("=====================")
    
    client = GmailClient()
    
    try:
        print("\n🔐 Authenticating with Gmail...")
        client.authenticate()
        print("✅ Authentication successful!")
        
        while True:
            print("\n📫 Recent Emails:")
            print("-" * 40)
            
            emails, _ = client.get_email_list(max_results=10)
            
            if not emails:
                print("No emails found.")
                break
            
            for i, email in enumerate(emails, 1):
                format_email_summary(email, i)
            
            print(f"\n📊 Showing {len(emails)} emails")
            
            # Get user choice
            try:
                choice = input("\nEnter email number to read (or 'q' to quit): ").strip()
                
                if choice.lower() == 'q':
                    break
                
                email_index = int(choice) - 1
                if 0 <= email_index < len(emails):
                    selected_email = emails[email_index]
                    print(f"\n📖 Loading email: {selected_email.subject}")
                    
                    detail = client.get_email_detail(selected_email.message_id)
                    format_email_detail(detail)
                    
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid email number.")
                    
            except ValueError:
                print("❌ Please enter a valid number or 'q' to quit.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    except ConfigurationError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project and enable Gmail API")
        print("3. Create OAuth2 credentials for desktop application")
        print("4. Download as 'credentials.json' in this directory")
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Try removing token.json and re-authenticating")
        
    except ConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("💡 Check your internet connection and try again")
        
    except ServiceError as e:
        print(f"❌ Gmail service error: {e}")
        print("💡 This might be a temporary issue, try again later")
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Please check the logs or contact support")
        
    finally:
        if client.is_authenticated():
            client.logout()
            print("🔓 Logged out successfully")


if __name__ == "__main__":
    main()
