# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def action_download_xsd_files(self):
        """
        Downloads the REPÚBLICA FEL XSD validation files
        if they don't already exist, for the active tax agency.
        """
        return super().action_download_xsd_files()
