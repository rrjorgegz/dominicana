{
    "name": "l10n_do_edi_fel",
    "summary": """
REPÚBLICA FEL
=============

    """,
    "author": "rrjorgegz",
    "website": "https://github.com/rrjorgegz",
    "category": "Accounting/Accounting/REPÚBLICA FEL",
    "version": "17.0.0.0.1",
    "depends": ["account_edi"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_view.xml",
        "views/res_config_settings_view.xml",
        "views/edi_env_view.xml",
        "data/edi_env_data.xml",
        "data/account_edi_data.xml",
        "data/template_invoice.xml",
        "views/account_move_view.xml",
    ],
    "external_dependencies": {
        "python": ["xmltodict"],
    },
    "license": "LGPL-3",
}
