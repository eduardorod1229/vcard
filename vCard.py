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
import qrcode
from io import BytesIO
import matplotlib.pyplot as plt


def format_phone_number(phone, phone_type):
    return f"+{phone}" if phone_type == 'Mobile' else f"{phone}"

def generate_vcard_qr_code(name, organization, job_title,cellphone, office_phone, emails, websites):
    vcard_data = f"BEGIN:VCARD\n" \
                 f"VERSION:3.0\n" \
                 f"FN:{name}\n" \
                 f"ORG:{organization}\n" \
                 f"TITLE:{job_title}\n" \
                 f"TEL;TYPE=CELL:{format_phone_number(cellphone, 'Mobile')}\n" \
                 f"TEL;TYPE=WORK:{format_phone_number(office_phone, 'Work')}\n"

    for email in emails:
        vcard_data += f"EMAIL:{email}\n"

    for website in websites:
        vcard_data += f"URL:{website}\n"

    vcard_data += "END:VCARD"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )

    qr.add_data(vcard_data)
    qr.make(fit=True)

    pil_image = qr.make_image(fill_color="black", back_color="white")


    img_bytes = BytesIO()
    pil_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Display the image using st.image
    st.image(img_bytes, caption='VCard', width=250)

    st.download_button(
        label='Download QR Code',
        data=img_bytes.getvalue(),
        file_name = 'vCard_qr_code.png',
        mime='image/png')

def main():
    st.title('vCard QR Code Generator')

    name = st.text_input('Name:')
    organization = st.text_input('Organization:')
    job_title = st.text_input('Job Title:')
    
    cellphone = st.text_input('Mobile:')
    office_phone = st.text_input('Work Phone:')

    emails = st.text_area('Emails (separate by commas):').split(',')
    websites = st.text_area('Websites (separate by commas):').split(',')

    if st.button('Generate QR Code'):
        generate_vcard_qr_code(name, organization, job_title, cellphone, office_phone, emails, websites)

if __name__ == '__main__':
    main()
