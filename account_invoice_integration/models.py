from odoo import models, fields, api

class AccountInvoiceIntegration(models.Model):
    _name = 'account.invoice.integration'
    _description = 'Integração de Faturas com Sistema Externo'

    invoice_id = fields.Many2one('account.move', string='Fatura no Odoo')
    external_system_id = fields.Char(string='ID da Fatura no Sistema Externo')
    status = fields.Selection([
        ('pendente', 'Pendente'),
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
    ], default='pendente', string='Status da Integração')
    response_message = fields.Text(string='Mensagem de Resposta do Sistema Externo')

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def action_post(self):
        result = super(AccountMove, self).action_post()
        for invoice in self:
            integration_data = {
                'invoice_id': invoice.id,
                'external_system_id': 'ID_da_Fatura_no_Sistema_Externo',
                'status': 'sucesso',
                'response_message': 'Mensagem de resposta do sistema externo',
            }
            self.env['account.invoice.integration'].create(integration_data)

        return result