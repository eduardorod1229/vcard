# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import segno
from io import BytesIO

def format_phone_number(phone, phone_type):
    return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"

def generate_vcard_qr_code(last_name, first_name, display_name, organization, urls, emails, phone, address, notes):
    vcard_data = f"BEGIN:VCARD\n" \
                 f"VERSION:3.0\n" \
                 f"N:{last_name};{first_name}\n" \
                 f"FN:{display_name}\n" \
                 f"ORG:{organization}\n"
    
    vcard_data += f"TEL;TYPE=mobile:{format_phone_number(phone, 'Work')}\n" \
                  f"ADR;TYPE=intl,work,postal,parcel:;;{address}\n" \
                  f"NOTE:{notes}\n" \
                  f"END:VCARD"

    for email in emails:
        vcard_data += f"EMAIL:{email}\n"
    
    for url in urls:
        vcard_data += f"URL:{url}\n"

   
    # Generate QR code using segno
    qr = segno.make(vcard_data)

  
    img_bytes = BytesIO()
    qr.save(img_bytes, kind='png', scale=5)

    # Display the image using st.image
    st.image(img_bytes, caption='VCard', width=250)

    # Download button
    st.download_button(
        label='Download QR Code',
        data=img_bytes.getvalue(),
        file_name='vCard_qr_code.png',
        mime='image/png'
    )

def main():
    st.title('vCard QR Code Generator')

    last_name = st.text_input('Last Name:')
    first_name = st.text_input('First Name:')
    display_name = st.text_input('Display Name:')
    organization = st.text_input('Organization:')
    phone = st.text_input('Mobile:')
    emails = st.text_area('Emails (separate by commas):').split(',')
    address = st.text_input('Address:')
    urls = st.text_area('URLs (separate by commas):').split(',')
    notes = st.text_area('Notes:')

    if st.button('Generate QR Code'):
        generate_vcard_qr_code(last_name, first_name, display_name, organization, urls, emails, phone, address, notes)

if __name__ == '__main__':
    main()
