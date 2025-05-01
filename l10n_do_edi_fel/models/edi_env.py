from odoo import api, fields, models


class EdiEnv(models.Model):
    _name = "edi.env"
    _description = "Enviroment of Electronic Data Interchange"

    name = fields.Char()
    server = fields.Char()
    active = fields.Boolean(default=True)

    @api.depends("server", "active")
    def _l10n_do_edi_env_is_valid(self):
        for record in self:
            if not record.active:
                return True
        return False
