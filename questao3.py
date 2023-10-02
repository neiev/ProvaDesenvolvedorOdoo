# Questão 3: Módulo de Contabilidade do Odoo

# Suponha que você esteja desenvolvendo um sistema de contabilidade para uma empresa com operações internacionais.

# A empresa lida com várias moedas e precisa de uma funcionalidade para converter automaticamente transações em diferentes moedas para a moeda base da empresa.

# Tarefa:

# 1) Crie um novo modelo chamado `account.foreign.exchange.rate` que permita o registro de taxas de câmbio entre diferentes moedas. O modelo deve conter os seguintes campos:

# a) `date` (Date): Data da taxa de câmbio.

# b) `currency_from_id` (Many2one): Moeda de origem.

# c) `currency_to_id` (Many2one): Moeda de destino.

# d) `exchange_rate` (Float): Taxa de câmbio.

# 2) Modifique o modelo `account.move` para incluir um campo `currency_id` que represente a moeda em que a transação está sendo registrada. Certifique-se de que este campo esteja relacionado com o modelo `res.currency`.

# 3) Implemente uma função no Odoo que, ao criar um lançamento contábil, verifique se a moeda da transação é diferente da moeda base da empresa. Em caso afirmativo, a função deve converter o valor da transação para a moeda base usando a taxa de câmbio correspondente.

# Observações:

# - Considere que os modelos `res.currency` e `account.move` já estão definidos no sistema.



from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountForeignExchangeRate(models.Model):
    _name = 'account.foreign.exchange.rate'
    _description = 'Taxas de câmbio entre moedas'

    date = fields.Date(string='Data da Taxa de Câmbio', required=True)
    currency_from_id = fields.Many2one('res.currency', string='Moeda de Origem', required=True)
    currency_to_id = fields.Many2one('res.currency', string='Moeda de Destino', required=True)
    exchange_rate = fields.Float(string='Taxa de Câmbio', required=True)

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_id = fields.Many2one('res.currency', string='Moeda da Transação', required=True)

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            exchange_rate = self.env['account.foreign.exchange.rate'].search([
                ('currency_from_id', '=', self.currency_id.id),
                ('currency_to_id', '=', self.company_id.currency_id.id),
                ('date', '<=', self.date),
            ], order='date desc', limit=1)

            if not exchange_rate:
                raise UserError(_("Não foi encontrada uma taxa de câmbio para converter para a moeda base."))

            self.amount_total = self.amount_total / exchange_rate.exchange_rate

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        move._onchange_currency_id()
        return move