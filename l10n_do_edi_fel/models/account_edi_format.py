import json

import requests
import xmltodict

from odoo import models


class AccountEdiFormat(models.Model):
    _inherit = "account.edi.format"

    def _is_compatible_with_journal(self, journal):
        # EXTENDS account.edi.format
        # For DO include the journals for sales invoices
        if self.code != "do_fel":
            return super()._is_compatible_with_journal(journal)
        return journal.country_code == "DO" and (
            (journal.type == "sale" and journal.l10n_latam_use_documents)
            or (journal.type == "general")
            or (journal.type == "purchase")
        )

    def _needs_web_services(self):
        return self.code == "do_fel" or super()._needs_web_services()

    def _get_move_applicability(self, move):
        # EXTENDS account_edi
        self.ensure_one()
        if self.code != "do_fel" or move.country_code != "DO":
            return super()._get_move_applicability(move)
        return {
            "post": self._l10n_do_edi_post_invoice(move),
            "cancel": "",
            "post_batching": "",
            "cancel_batching": "",
            "edi_content": "",
        }

    def _l10n_do_edi_post_invoice(self, move):
        # PASO 1: GENERAR XML (usando template)
        xml_content = self._l10n_do_edi_post_invoice_generate_xml(move)
        # PASO 2: ENVIAR XML
        self._l10n_do_edi_post_invoice_send_xml(xml_content, move.company_id)

    def _l10n_do_edi_post_invoice_generate_xml(self, move):
        doc_type = move.l10n_latam_document_type_id.internal_type
        template = {
            "credit_note": "l10n_do_edi_fel.template_invoice_post",
            "debit_note": "l10n_do_edi_fel.template_invoice_post",
            "invoice": "l10n_do_edi_fel.template_invoice_post",
            "purchase_liquidation": "l10n_do_edi_fel.template_invoice_post",
        }[doc_type]
        # Create values {'inv': move}
        values = self._values_edi_fel(move)
        # Generate XML document
        xml_content = self.env["ir.qweb"]._render(template, values).encode().decode()
        xml_content = xmltodict.parse(xml_content)["Request"]
        # # Limpiar los datos del xml
        # xml_content = self.cleanup_xml_node(xml_content)
        # Comprobar si xml es valido con los xsd
        errors = self._l10n_do_validate_with_xsd(xml_content, doc_type)
        # # Firmar el xml antes de enviar
        # if move.company_id._l10n_ec_is_demo_environment():
        # # unless we're in a test environment without certificate
        #     xml_signed = etree.tostring(xml_content, encoding='unicode')
        # else:
        #     xml_signed = move.company_id.sudo().
        # l10n_ec_edi_certificate_id._action_sign(xml_content)

        # xml_content = '<?xml version="1.0" encoding="UTF-8"?>' + xml_content
        return xml_content, errors

    # def cleanup_xml_node(self, xml_content):
    #     return xml_content

    def _l10n_do_validate_with_xsd(self, xml_content, doc_type):
        return True

    def _l10n_do_edi_post_invoice_send_xml(self, xml_content, company_id):
        # SEND XML POST
        headers = {"accept": "*/*", "content-type": "application/json; charset=UTF-8"}
        response = requests.post(
            company_id.l10n_do_edi_production_env,
            data=json.dumps(xml_content),
            headers=headers,
            timeout=(10, 30),
        )
        return json.loads(response.content.decode())

    def _values_edi_fel(self, move):
        tipo_pago = {"01": 1, "02": 2, "03": 2, "04": 2, "05": 3, "06": 2, "07": 3}
        return {"inv": move, "tipo_pago": tipo_pago["01"]}
