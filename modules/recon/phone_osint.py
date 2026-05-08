---

### File: `phone_osint.py`

```python
#!/usr/bin/env python3
"""
Phone number OSINT recon tool.
Gathers carrier, location, timezone, and availability intel from a phone number.
"""
import argparse
import sys
import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberType
from phonenumbers import number_format

def banner():
    print("""
╔══════════════════════════════════════╗
║   Phone OSINT Recon Tool            ║
║   Authorized Pentesting Use Only    ║
╚══════════════════════════════════════╝
""")

def enumerate_number(number_str):
    try:
        # Parse with country code detection
        parsed = phonenumbers.parse(number_str, None)
        
        # Also try with US default if no country code
        if not parsed.country_code:
            parsed = phonenumbers.parse(number_str, "US")
        
        print(f"\n[+] Target: {number_str}")
        print(f"[+] E.164 Format: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"[+] National Format: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        print(f"[+] International: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        
        # Country
        country = geocoder.country_name_for_number(parsed, "en")
        print(f"[+] Country: {country}")
        
        # Location (region/city)
        location = geocoder.description_for_number(parsed, "en")
        print(f"[+] Location: {location}")
        
        # Carrier
        carrier_name = carrier.name_for_number(parsed, "en")
        if carrier_name:
            print(f"[+] Carrier: {carrier_name}")
        else:
            print(f"[!] Carrier: Unknown (may be landline or VoIP)")
        
        # Timezones
        tzones = timezone.time_zones_for_number(parsed)
        print(f"[+] Timezone(s): {', '.join(tzones)}")
        
        # Number type
        num_type = phonenumbers.number_type(parsed)
        type_names = {
            PhoneNumberType.FIXED_LINE: "Fixed Line",
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            PhoneNumberType.TOLL_FREE: "Toll Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.SHARED_COST: "Shared Cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.VOICEMAIL: "Voicemail",
            PhoneNumberType.UNKNOWN: "Unknown",
        }
        print(f"[+] Number Type: {type_names.get(num_type, 'Unknown')}")
        
        # Validation
        print(f"[+] Valid: {phonenumbers.is_valid_number(parsed)}")
        print(f"[+] Possible: {phonenumbers.is_possible_number(parsed)}")
        
        # Country code and national number
        print(f"[+] Country Code: +{parsed.country_code}")
        print(f"[+] National Number: {parsed.national_number}")
        
        # Check if it's a mobile number (relevant for MMS delivery)
        is_mobile = num_type in (PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE)
        print(f"[+] SMS/MMS Capable: {'Yes' if is_mobile else 'Likely VoIP/Landline'}")
        
        return parsed
        
    except Exception as e:
        print(f"[-] Error parsing number: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phone OSINT Reconnaissance Tool")
    parser.add_argument("--number", "-n", required=True, help="Phone number with country code (e.g., +15098735206)")
    args = parser.parse_args()
    
    banner()
    enumerate_number(args.number)