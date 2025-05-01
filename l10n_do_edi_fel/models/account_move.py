# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Stored XML Binaries
    l10n_do_fel_post_xml = fields.Binary(
        attachment=True,
        readonly=True,
        copy=False,
        string="Submission XML",
        help="""Submission XML sent to REPÚBLICA FEL. Kept if
        accepted or no response (timeout), cleared otherwise.""",
    )
    l10n_do_fel_cancel_xml = fields.Binary(
        attachment=True,
        readonly=True,
        copy=False,
        string="Cancellation XML",
        help="""Cancellation XML sent to REPÚBLICA FEL. Kept if
        accepted or no response (timeout), cleared otherwise.""",
    )

    # -------------------------------------------------------------------------
    # API-DECORATED & EXTENDED METHODS
    # -------------------------------------------------------------------------

    # @api.depends('state', 'edi_document_ids.state')
    # def _compute_show_reset_to_draft_button(self):
    #     # EXTENDS account_edi account.move
    #     super()._compute_show_reset_to_draft_button()

    # for move in self:
    #     if move.l10n_es_tbai_chain_index:
    # move.show_reset_to_draft_button = False

    # def button_draft(self):
    #     # EXTENDS account account.move
    #     for move in self:
    #         if not move.edi_state == 'cancelled':
    #             raise UserError(_("""You cannot reset to draft an entry
    #                 that has been posted to REPÚBLICA FEL's chain"""))
    #     super().button_draft()

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------

    def _l10n_es_tbai_is_in_chain(self):
        """
        True iff invoice has been posted to the chain and confirmed by govt.
        Note that cancelled invoices remain part of the chain.
        """
        fel_doc_ids = self.edi_document_ids.filtered(
            lambda d: d.edi_format_id.code == "do_fel"
        )
        return len(fel_doc_ids) > 0 and not any(
            fel_doc_ids.filtered(lambda d: d.state == "to_send")
        )
