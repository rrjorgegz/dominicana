from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_do_edi_username = fields.Char(
        string="E-invoice (DO) username",
        related="company_id.l10n_do_edi_username",
        readonly=False,
    )
    l10n_do_edi_password = fields.Char(
        string="E-invoice (DO) password",
        related="company_id.l10n_do_edi_password",
        readonly=False,
    )
    l10n_do_edi_production_env = fields.Char(
        string="E-invoice (DO) EDI Server Environment",
        compute="_compute_l10n_do_edi_production_env",
        store=True,
    )

    @api.depends("company_id")
    def _compute_l10n_do_edi_production_env(self):
        for record in self:
            record.l10n_do_edi_production_env = ""
            if record.company_id.l10n_do_edi_production_env:
                record.l10n_do_edi_production_env = (
                    record.company_id.l10n_do_edi_production_env
                )
