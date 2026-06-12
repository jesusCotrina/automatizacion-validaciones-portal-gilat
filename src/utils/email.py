import locale
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
import mimetypes
from datetime import datetime
import zipfile
import os
import logging

logger = logging.getLogger(__name__)

def enviar_correo(
    resultados: dict,
    asunto: str,
    destinatarios: str,
    path_archivo
):
    
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = "reportes-notas-de-credito@gilatla.com"
    msg["To"] = destinatarios

    logger.info("Construyendo el cuerpo del correo...")
    logo_cid = make_msgid(domain="gilatla.com")

    html_body = build_email_body(resultados,logo_cid)
    msg.set_content("Correo HTML.")
    msg.add_alternative(html_body, subtype="html")

    with open("assets/logo_gilat.jpg", "rb") as img:
        img_data = img.read()

    msg.get_payload()[1].add_related(
        img_data,
        maintype="image",
        subtype="jpeg",
        cid=logo_cid
    )

    # -------------------------
    # ADJUNTAR ZIP
    # -------------------------

    with open(path_archivo, "rb") as f:

        file_data = f.read()

        mime_type, _ = mimetypes.guess_type(path_archivo)

        maintype, subtype = mime_type.split("/")

        msg.add_attachment(
            file_data,
            maintype=maintype,
            subtype=subtype,
            filename=os.path.basename(path_archivo)
        )

    with smtplib.SMTP("mail.gilatla.com", 25) as smtp:
        smtp.send_message(msg)
    logger.info(f"Correo enviado a: {destinatarios} con asunto: '{asunto}' y adjunto: '{path_archivo}'")

def build_html_table(resultados: dict) -> str:
    rows = ""

    for idx, data in enumerate(resultados, start=1):
        mensaje_proceso = data.get("estado", "")
        is_ok = "OK" in mensaje_proceso
        status_color = "#2E7D32" if is_ok else "#C62828"
        status_label = "OK" if is_ok else "ERROR"
        rows += f"""
        <tr>
            <td style="padding:10px;border-bottom:1px solid #E0E0E0;text-align:center;">
                {idx}
            </td>
            <td style="padding:10px;border-bottom:1px solid #E0E0E0;">
                {data['region']}
            </td>
            <td style="padding:10px;border-bottom:1px solid #E0E0E0;color:{status_color};">
                <b>{status_label}</b> – {data['mensaje']}
            </td>
        </tr>
        """

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-collapse:collapse;font-family:Arial;font-size:13px;">
        <thead>
            <tr style="background-color:#2B0A5A;color:#FFFFFF;">
                <th style="padding:12px;text-align:center;">#</th>
                <th style="padding:12px;text-align:left;">Proceso</th>
                <th style="padding:12px;text-align:left;">Resultado</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


def build_email_body(resultados, logo_cid   ):
    table_html = build_html_table(resultados)
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain')

    fecha = datetime.now().strftime("%d de %B de %Y")
    

    return f"""
    <html>
    <body style="margin:0;padding:0;background-color:#F5F6FA;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center">

                    <!-- CONTENEDOR -->
                    <table width="680" cellpadding="0" cellspacing="0"
                           style="background-color:#FFFFFF;margin:30px auto;
                                  border-radius:6px;overflow:hidden;">

                        <!-- HEADER -->
                        <tr>
                            <td style="background-color:#1f0050;padding:25px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td width="80"
                                            valign="middle"
                                            style="padding-right:20px;">
                                            
                                            <img src="cid:{logo_cid[1:-1]}" 
                                                alt="Gilat"
                                                width="140"
                                                style="display:block;
                                                        height:60px;
                                                        width:auto;
                                                        max-width:160px;">
                                        </td>

                                        <!-- TEXTO -->
                                        <td valign="middle">
                                            <span style="color:#00D4C7;
                                                        font-size:13px;
                                                        font-weight:bold;
                                                        font-family:Arial;">
                                                {fecha}
                                            </span>

                                            <h1 style="color:#FFFFFF;
                                                    font-family:Arial;
                                                    font-size:24px;
                                                    margin:8px 0 0 0;">
                                                Generación de Reportes Notas de Crédito
                                            </h1>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- BODY -->
                        <tr>
                            <td style="padding:30px;color:#333333;font-family:Arial;
                                       font-size:14px;line-height:1.6;">
                                <p>Estimados,</p>

                                <p>
                                    Se ha ejecutado el proceso
                                    <b>Generación de Reportes Notas de Credito</b>.
                                    A continuación, se presenta el resumen de los resultados obtenidos:
                                </p>

                                <div style="margin:20px 0;">
                                    {table_html}
                                </div>

                                <p style="margin-top:30px;">
                                    Los reportes generados se encuentran adjuntos en el zip de este correo.<br>
                                    <br>
                                    Saludos cordiales,<br>
                                    <b>IT Infrastructure</b>
                                </p>
                            </td>
                        </tr>

                        <!-- FOOTER -->
                        <tr>
                            <td style="background-color:#2B0A5A;color:#FFFFFF;
                                       padding:15px;text-align:center;
                                       font-size:12px;">
                                © Gilat Satellite Networks - Internal Use Only
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>
    </body>
    </html>
    """