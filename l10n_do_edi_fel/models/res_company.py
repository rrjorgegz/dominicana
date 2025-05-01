from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_do_edi_username = fields.Char(
        string="E-invoice (DO) Username",
        groups="base.group_system",
    )
    l10n_do_edi_password = fields.Char(
        string="E-invoice (DO) Password",
        groups="base.group_system",
    )
    l10n_do_edi_env = fields.Many2one(
        "edi.env",
        string="E-invoice (DO) EDI environment",
        help="Enable the use of production credentials",
        groups="base.group_system",
        domain="[('active','=',True)]",
    )
    l10n_do_edi_production_env = fields.Char(
        string="E-invoice (DO) Server EDI",
        compute="_compute_l10n_do_edi_production_env",
        store=True,
    )

    @api.depends("l10n_do_edi_env")
    def _compute_l10n_do_edi_production_env(self):
        for record in self:
            record.l10n_do_edi_production_env = ""
            if record.l10n_do_edi_env:
                record.l10n_do_edi_production_env = record.l10n_do_edi_env.server
